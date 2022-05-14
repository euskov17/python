import typing as tp


def filter_list_by_list(lst_a: tp.Union[list[int], range],
                        lst_b: tp.Union[list[int], range]) -> list[int]:
    """
        Filter first sorted list by other sorted list
        :param lst_a: first sorted list
        :param lst_b: second sorted list
        :return: filtered sorted list
        """
    result = []
    it_b = 0
    for it_a in range(len(lst_a)):
        while it_b < len(lst_b) - 1 and lst_a[it_a] > lst_b[it_b]:
            it_b += 1
        if it_b == len(lst_b) or lst_a[it_a] != lst_b[it_b]:
            result.append(lst_a[it_a])
    return result
