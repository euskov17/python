import typing as tp


def find_value(nums: tp.Union[list[int], range], value: int) -> bool:
    """
        Find value in sorted sequence
        :param nums: sequence of integers. Could be empty
        :param value: integer to find
        :return: True if value exists, False otherwise
    """
    print(nums, end='\n')
    length = len(nums)
    if length == 0:
        return False
    if (mid_value := nums[length//2]) == value:
        return True
    if length == 1:
        return False
    if mid_value < value:
        return find_value(nums[length//2:], value)
    else:
        return find_value(nums[:length//2], value)
