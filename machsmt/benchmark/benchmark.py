import os
import time
from collections.abc import Iterable

from machsmt.util import die, warning
from .tokenize_sexpr import SExprTokenizer
from ..features import bonus_features
from ..config import args
from func_timeout import func_timeout, FunctionTimedOut
from ..smtlib import get_relevant_constructs

class Benchmark:
    def __init__(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Could not find: {path}")
        self.path = path
        self.features = []
        self.logic = 'UNPARSED'
        self.parsed = False
        self.total_feature_time = 0.0
        self.relevant_constructs = []
        self.construct_to_index = {}

        self.solvers = {}
        self.scores = {}

    def get_path(self):
        return self.path

    def get_solvers(self):
        return sorted(self.solvers.values(), key=lambda p: p.get_name())

    def add_solver(self, solver, score):
        self.solvers[solver.get_name()] = solver
        self.scores[solver.get_name()] = score

    def get_score(self, solver):
        return self.scores[solver.get_name()]

    def get_logic(self): 
        return self.logic

    # Compute Features up to a timeout
    def compute_features(self):
        start = time.time()

        self.compute_core_features()

        if False and args.semantic:
            self.compute_semantic_features()

        self.total_feature_time = time.time() - start

    def compute_core_features(self):
        assert hasattr(self, 'tokens')
        
        # Handle the case where logic might not be set
        if self.logic == 'UNSET_LOGIC' or self.logic == 'UNPARSED':
            # Default to a full feature set if no logic is specified
            self.logic = 'DEFAULT'
        
        # Get relevant constructs based on the logic
        self.relevant_constructs = get_relevant_constructs(self.logic)
        
        # Create mapping from construct to index
        self.construct_to_index = dict((self.relevant_constructs[i], i) for i in range(len(self.relevant_constructs)))
        
        # Initialize feature vector
        self.features = [0] * (len(self.relevant_constructs) + 2)
        
        # Set file size feature
        self.features[-1] = float(os.path.getsize(self.path))

        def count_occurrences(sexprs, features, construct_to_index):
            visit = sexprs[:]
            while visit:
                cur = visit.pop()
                if isinstance(cur, tuple):
                    visit.extend(cur)
                elif isinstance(cur, str):
                    if cur in construct_to_index:
                        features[construct_to_index[cur]] += 1
                else:
                    die(f"parsing error on: {self.path} {str(type(cur))}")

        try:
            func_timeout(timeout=args.feature_timeout,
                         func=count_occurrences,
                         args=(self.tokens, self.features, self.construct_to_index))
        except FunctionTimedOut:
            warning(
                f'Timeout after {args.feature_timeout} seconds of compute_core_features on {self}')
            self.features[-2] = 1
        except RecursionError:
            print(f"Recursion Error on :{self}")

    def compute_semantic_features(self):
        assert hasattr(self, 'tokens')
        timeout = (args.feature_timeout / 2.0) / len(bonus_features)
        for feat in bonus_features:
            try:
                ret = func_timeout(timeout=timeout,
                                   func=feat,
                                   args=(self.tokens,))
                if isinstance(ret, Iterable):
                    for r in ret:
                        self.features.append(float(r))
                else:
                    self.features.append(float(ret))
            except (FunctionTimedOut, RecursionError):
                ret = feat([])
                if isinstance(ret, Iterable):
                    for r in ret:
                        self.features.append(-1.0)
                else:
                    self.features.append(-1.0)
                warning('Timeout after {} seconds of {} on {}'.format(
                    timeout, feat.__name__, self.path))

    # Get and if necessary, compute features.
    def get_features(self):
        return self.features
    
    # Get the relevant constructs for this benchmark
    def get_relevant_constructs(self):
        return self.relevant_constructs
    
    # Get the feature names in order
    def get_feature_names(self):
        """Return the names of the features in the order they appear in the feature vector."""
        # Create a list of the same length as features
        names = [''] * len(self.features)
        
        # Fill in the construct names based on their indices
        for construct, idx in self.construct_to_index.items():
            names[idx] = construct
            
        # Add names for the special features at the end
        names[-2] = 'timeout_flag'
        names[-1] = 'file_size'
        
        return names

    def parse(self):
        assert not hasattr(self, 'tokens')
        self.tokens = [sexpr for sexpr in SExprTokenizer(self.path)]
        self.logic = 'UNSET_LOGIC'
        for sexpr in self.tokens:
            if len(sexpr) >= 2 and sexpr[0] == 'set-logic':
                self.logic = sexpr[1]
                break
        self.compute_features()
        del self.tokens
        assert not hasattr(self, 'tokens')

    def __str__(self): 
        return f"Benchmark(self.path={self.path}, len(self.solvers)={len(self.solvers)}, self.logic={self.logic})"
    __repr__ = __str__

    def __hash__(self):
        return hash(str(self))