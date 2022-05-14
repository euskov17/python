def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    result = []
    it_a = 0
    it_b = 0
    while it_a < len(lst_a) and it_b < len(lst_b):
        if lst_a[it_a] < lst_b[it_b]:
            result.append(lst_a[it_a])
            it_a += 1
        else:
            result.append(lst_b[it_b])
            it_b += 1
    if it_a == len(lst_a):
        while it_b < len(lst_b):
            result.append(lst_b[it_b])
            it_b += 1
    else:
        while it_a < len(lst_a):
            result.append(lst_a[it_a])
            it_a += 1
    return result


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list ising `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    return sorted(lst_a + lst_b)
