def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule,
    that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of
                [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of
                [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type,
    which can be used to convert both input values
    """
    if type1 == type2 and type1 == range:
        return tuple
    if type2 == list and type1 == range:
        return list
    if type1 == list and type2 not in [range, list, tuple]:
        return str
    if type2 == list and type1 not in [list, range, tuple]:
        return str
    if type1 == list or type2 == list:
        return list
    if type1 == tuple and type2 in [bool, int, float, complex]:
        return str
    if type2 == tuple and type1 in [bool, int, float, complex]:
        return str
    if type1 == range and type2 in [bool, int, float, complex]:
        return str
    if type2 == range and type1 in [bool, int, float, complex]:
        return str
    print("Hello world")
    it_1 = 0
    it_2 = 0
    types = [bool, int, float, complex, list, range, tuple, str]
    for ind in range(len(types)):
        if types[ind] == type1:
            it_1 = ind
        if types[ind] == type2:
            it_2 = ind
    return types[max(it_1, it_2)]
