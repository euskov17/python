def reverse_iterative(lst: list[int]) -> list[int]:
    """
    Return reversed list. You can use only iteration
    :param lst: input list
    :return: reversed list
    """
    result = []
    for i in range(length := len(lst)):
        result.append(lst[length - i - 1])
    return result


def reverse_inplace_iterative(lst: list[int]) -> None:
    """
    Revert list inplace. You can use only iteration
    :param lst: input list
    :return: None
    """
    for i in range((length := len(lst)) // 2):
        lst[i], lst[length - i - 1] = lst[length - i - 1], lst[i]


def reverse_inplace(lst: list[int]) -> None:
    """
    Revert list inplace with reverse method
    :param lst: input list
    :return: None
    """
    lst.reverse()


def reverse_reversed(lst: list[int]) -> list[int]:
    """
    Revert list with `reversed`
    :param lst: input list
    :return: reversed list
    """
    return list(reversed(lst))


def reverse_slice(lst: list[int]) -> list[int]:
    """
    Revert list with slicing
    :param lst: input list
    :return: reversed list
    """
    print(lst)
    if (length := len(lst)) == 1:
        return [lst[0]]
    if length == 0:
        return []
    diff = 0
    mid_el = []
    if length % 2 == 1:
        diff = 1
        mid_el.append(length // 2 + 1)
    return reverse_slice(lst[length // 2 + diff:]) + \
        mid_el + reverse_slice(lst[:length // 2])
