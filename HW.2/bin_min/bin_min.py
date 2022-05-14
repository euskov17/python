import typing as tp


def find_min(nums: tp.Sequence[int]) -> int:
    """
    Find minimum in rotated not empty sorted sequence without dublicates.
    :param nums: sequence of integer
    :return: minimum value
    """
    index = 0
    deg = len(nums)
    while nums[index] > nums[(index - 1) % (length := len(nums))] \
            or nums[index] > nums[(index + 1) % length]:
        if deg != 1:
            deg //= 2
        if nums[(index + deg) % length] > nums[index] or deg <= 1:
            index += deg
    return nums[index]
