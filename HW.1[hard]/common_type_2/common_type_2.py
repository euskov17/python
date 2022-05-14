import typing as tp


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert
    each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """
    types: list[type] = [str, bool, int, float, list, tuple]
    max_type = 0
    for el in data:
        it = 0
        while it <= 5 and types[it] != type(el):
            it += 1
        cur_type = it
        if cur_type == 6:
            cur_type = -1
        if cur_type == 2 and el in [0, 1]:
            if max_type in [0, 1]:
                cur_type = 1
        if el or (el == 0):
            print(f'max_type = {max_type} cur_type = {cur_type}')
            it = 0
            while it != cur_type and it != max_type:
                it += 1
            if it == max_type:
                max_type = cur_type
    result: list[tp.Any] = []
    if max_type == 5 or max_type == 4:
        for el in data:
            if not el:
                result.append([])
            elif type(el) == tuple:
                result.append([elem for elem in el])
            elif type(el) != list:
                result.append([el])
            else:
                result.append(el)
        return result
    if max_type == 0:
        for el in data:
            if not el:
                result.append("")
            else:
                result.append(el)
    if max_type in [2, 3]:
        for el in data:
            if not el:
                result.append(types[max_type](0))
            else:
                result.append(types[max_type](el))
    if max_type == 1:
        flag = 1
        for el in data:
            if type(el) == int:
                flag = 0
            if type(el) == bool:
                flag = 1
        if flag == 0:
            for el in data:
                if not el:
                    result.append(0)
                else:
                    result.append(int(el))
        else:
            for el in data:
                if not el:
                    result.append(False)
                else:
                    result.append(bool(el))
    return result
