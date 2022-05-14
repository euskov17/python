import typing as tp


def find_peak_index(nums: tp.Sequence[int]) -> int:
    """
    Find `peak` value in sequence and return its index.
    Peak means that both neighbours are less or equals to value.
    :param nums: sequence of integers
    :return: index of peak value
    """
    index = (length := len(nums)) // 2
    while (index != 0 and nums[index] < nums[(index + 1) % length]) or \
            (index != length - 1 and nums[index] < nums[(index - 1) % length]):
        if nums[index] < nums[(index - 1) % length]:
            return find_peak_index(nums[:index])
        else:
            return index + 1 + find_peak_index(nums[index + 1:])
    return index
