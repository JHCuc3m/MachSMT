# General SMT-LIB Keywords (Command Language)
command_keywords = [
    'as', 'assert', 'check-sat', 'check-sat-assuming', 'declare-const',
    'declare-datatype', 'declare-datatypes', 'declare-fun', 'declare-sort',
    'define-fun', 'define-fun-rec', 'define-funs-rec', 'define-sort',
    'echo', 'exit', 'get-assertions', 'get-assignment', 'get-info',
    'get-model', 'get-option', 'get-proof', 'get-unsat-assumptions',
    'get-unsat-core', 'get-value', 'pop', 'push', 'reset',
    'reset-assertions', 'set-info', 'set-logic', 'set-option',
]

# Quantifiers and Binders
binders = [
    'exists', 'forall', 'let',
]

# Core Theory (Boolean Logic)
core_theory = [
    'true', 'false', 'not', '=>', 'and', 'or', 'xor',
    '=', 'distinct', 'ite', 'Bool',
]

# Arrays Theory
arrays_theory = [
    'Array', 'select', 'store',
]

# Bit-Vectors Theory
bitvectors_theory = [
    'BitVec', 'concat', 'extract', 'bvnot', 'bvand', 'bvor', 'bvneg',
    'bvadd', 'bvmul', 'bvudiv', 'bvurem', 'bvshl', 'bvlshr', 'bvult',
    'bvnand', 'bvnor', 'bvxor', 'bvxnor', 'bvcomp', 'bvsub', 'bvsdiv',
    'bvsrem', 'bvsmod', 'bvashr', 'repeat', 'zero_extend', 'sign_extend',
    'rotate_left', 'rotate_right', 'bvule', 'bvugt', 'bvuge', 'bvslt',
    'bvsle', 'bvsgt', 'bvsge',
]

# Floating-Point Theory
floating_point_theory = [
    'RoundingMode', 'FloatingPoint', 'Float16', 'Float32', 'Float64', 'Float128',
    'fp', 'roundNearestTiesToEven', 'roundNearestTiesToAway', 'roundTowardPositive',
    'roundTowardNegative', 'roundTowardZero', 'RNE', 'RNA', 'RTP', 'RTN', 'RTZ',
    'fp.abs', 'fp.neg', 'fp.add', 'fp.sub', 'fp.mul', 'fp.div', 'fp.fma',
    'fp.sqrt', 'fp.rem', 'fp.roundToIntegral', 'fp.min', 'fp.max', 'fp.leq',
    'fp.lt', 'fp.geq', 'fp.gt', 'fp.eq', 'fp.isNormal', 'fp.isSubnormal',
    'fp.isZero', 'fp.isInfinite', 'fp.isNaN', 'fp.isNegative', 'fp.isPositive',
    'to_fp', 'to_fp_unsigned', 'fp.to_ubv', 'fp.to_sbv', 'fp.to_real',
]

# Arithmetic Theory
arithmetic_theory = [
    'Int',
    'Real',
    '-',
    '+',
    '*',
    'div',
    'mod',
    'abs',
    '<=',
    '<',
    '>=',
    '>',
    'to_real',
    'to_int',
    'is_int',
]

# Strings and Regular Expressions Theory
strings_regex_theory = [
    'String', 'RegLan', "str.++", "str.len", "str.<", "str.to_re",
    "str.in_re", "re.none", "re.all", "re.allchar", "re.++",
    "re.union", "re.inter", "re.*", "str.<=", "str.at", "str.substr",
    "str.prefixof", "str.suffixof", "str.contains", "str.indexof",
    "str.replace", "str.replace_all", "str.replace_re", "str.replace_re_all",
    "re.comp", "re.diff", "re.opt", "re.range", "re.loop", "re.^",
    "str.is_digit", "str.to_code", "str.from_code", "str.to_int", "str.from_int",
]

# Uninterpreted Functions
uf_theory = [
    # UF doesn't have specific keywords beyond those in command_keywords
]

# Logic mapping to relevant theories - based on the provided graph
logic_to_theories = {
    # Quantifier-Free Logics
    'QF_UF': [uf_theory, core_theory],
    'QF_BV': [bitvectors_theory, core_theory],
    'QF_IDL': [arithmetic_theory, core_theory],
    'QF_RDL': [arithmetic_theory, core_theory],
    'QF_LIA': [arithmetic_theory, core_theory],
    'QF_LRA': [arithmetic_theory, core_theory],
    'QF_NIA': [arithmetic_theory, core_theory],
    'QF_NRA': [arithmetic_theory, core_theory],
    'QF_AX': [arrays_theory, core_theory],
    
    # Combinations of Quantifier-Free Logics
    'QF_UFIDL': [uf_theory, arithmetic_theory, core_theory],
    'QF_UFBV': [uf_theory, bitvectors_theory, core_theory],
    'QF_UFLIA': [uf_theory, arithmetic_theory, core_theory],
    'QF_UFLRA': [uf_theory, arithmetic_theory, core_theory],
    'QF_UFNIA': [uf_theory, arithmetic_theory, core_theory],
    'QF_UFNRA': [uf_theory, arithmetic_theory, core_theory],
    'QF_ABV': [arrays_theory, bitvectors_theory, core_theory],
    'QF_ALIA': [arrays_theory, arithmetic_theory, core_theory],
    'QF_AUFBV': [arrays_theory, uf_theory, bitvectors_theory, core_theory],
    'QF_AUFLIA': [arrays_theory, uf_theory, arithmetic_theory, core_theory],
    
    # Quantified Logics
    'LIA': [arithmetic_theory, core_theory, binders],
    'LRA': [arithmetic_theory, core_theory, binders],
    'NIA': [arithmetic_theory, core_theory, binders],
    'NRA': [arithmetic_theory, core_theory, binders],
    'UFLRA': [uf_theory, arithmetic_theory, core_theory, binders],
    'UFNIA': [uf_theory, arithmetic_theory, core_theory, binders],
    'ALIA': [arrays_theory, arithmetic_theory, core_theory, binders],
    'AUFLIA': [arrays_theory, uf_theory, arithmetic_theory, core_theory, binders],
    'AUFLIRA': [arrays_theory, uf_theory, arithmetic_theory, core_theory, binders],
    'AUFNIRA': [arrays_theory, uf_theory, arithmetic_theory, core_theory, binders],
    
    # Floating-point logics
    'QF_FP': [floating_point_theory, core_theory],
    
    # String logics
    'QF_S': [strings_regex_theory, core_theory],
    
    # Default case for unknown or unspecified logics
    'DEFAULT': [command_keywords, core_theory, arrays_theory, bitvectors_theory, 
               floating_point_theory, arithmetic_theory, 
               strings_regex_theory, uf_theory, binders]
}

def get_relevant_constructs(logic):
    """
    Get the list of relevant grammatical constructs for a given logic.
    
    Args:
        logic (str): The SMT logic (e.g., 'QF_BV', 'AUFLIA')
        
    Returns:
        list: Combined list of all relevant grammatical constructs for the logic
    """
    # Always include command keywords
    relevant_constructs = command_keywords.copy()
    
    # Add theory-specific keywords based on the logic
    if logic in logic_to_theories:
        theories = logic_to_theories[logic]
        for theory in theories:
            # Don't add command_keywords again if they're in theories
            if theory != command_keywords:
                for construct in theory:
                    if construct not in relevant_constructs:
                        relevant_constructs.append(construct)
    else:
        # If logic is unknown, use all constructs
        for theory in logic_to_theories['DEFAULT']:
            if theory != command_keywords:
                for construct in theory:
                    if construct not in relevant_constructs:
                        relevant_constructs.append(construct)
    
    return relevant_constructs