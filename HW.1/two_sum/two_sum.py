import typing as tp


def two_sum(nums: tp.Sequence[int], target: int) -> tp.List[int]:
    """
    Takes a list of integers, return indices of the two numbers
    such that they add up to a specific target.
    You may assume that each input would have exactly one solution,
    and you may not use the same element twice.
    :param nums: list of integers
    :param target: specific target
    :return: list of the two indices
    """
    for i in range(length := len(nums)):
        for j in range(i + 1, length):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
