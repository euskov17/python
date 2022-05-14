import typing as tp
from collections import defaultdict


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    visited = []
    new_dict: dict[str, list[str]] = dict(defaultdict(list[str]))
    for name, el in dct.items():
        print(name)
        if el not in visited:
            new_dict[el] = [name]
            visited.append(el)
        else:
            new_dict[el].append(name)
    return new_dict
