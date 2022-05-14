import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result = []
    for key_d, value_d in dct.items():
        # key = prefix + key_d
        if value_d is tuple:
            new_items = traverse_dictionary_immutable(dct[key_d]
                                                      , prefix + key_d)
            for el in new_items:
                result.append(el)
        else:
            result.append((prefix + key_d, value_d))
    return result

def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    for key_d, value_d in dct.items():
        # key = prefix + key_d
        if value_d is tuple:
            new_items = traverse_dictionary_immutable(dct[key_d]
                                                      , prefix + key_d)
            for el in new_items:
                result.append(el)
        else:
            result.append((prefix + key_d, value_d))


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
        ) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result = []
    for key_d, value_d in dct.items():
        key = [key_d]
        value = [value_d]
        visited = []
        for el in value:
            while el is tuple:
                for i in range(len(el.items())):
                    key.append((el.items())[0][i])
                    value.append(el.items()[0][i])
            result.append((key, value_d))