import typing as tp


def get_squares(elements: list[int]) -> list[int]:
    """
        :param elements: list with integer values
        :return: list with squared values
        """
    result = []
    for el in elements:
        result.append(el**2)
    return result


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
        :param elements: list with integer values
        :return: list with indices started from 1
        """
    return [1 + index for index in range(len(elements))]


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> tp.Optional[int]:
    """
        :param elements: list with integer values
        :return: index of maximum element if exists, None otherwise
        """
    if len(elements) == 0:
        return None
    max_el = elements[0]
    result = 0
    for i in range(len(elements)):
        if elements[i] > max_el:
            result = i
            max_el = elements[i]
    return result


# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
        :param elements: list with integer values
        :return: list with each second element of list
        """
    return [elements[2 * i + 1] for i in range(len(elements)//2)]


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> tp.Optional[int]:
    """
        :param elements: list with integer values
        :return: index of first "3" in the list if exists, None otherwise
        """
    for i in range(len(elements)):
        if elements[i] == 3:
            return i
    return None


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> tp.Optional[int]:
    """
        :param elements: list with integer values
        :return: index of last "3" in the list if exists, None otherwise
        """
    length = len(elements)
    for i in range(length):
        if elements[length - i - 1] == 3:
            return length - i - 1
    return None


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
        :param elements: list with integer values
        :return: sum of elements
        """
    return sum(elements)


# ====================================================================================================


def get_min_max(elements: list[int], default: tp.Optional[int])\
        -> tuple[tp.Optional[int], tp.Optional[int]]:
    """
        :param elements: list with integer values
        :param default: default value to return if elements are empty
        :return: (min, max) of list elements or
        (default, default) if elements are empty
    """
    if len(elements) == 0:
        return default, default
    return min(elements), max(elements)

# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int)\
        -> tp.Optional[int]:
    """
        :param elements: list with integer values
        :param i: index of elements to check with boundary
        :param boundary: boundary for check element value
        :return: element at index `i` from `elements` if element
        greater than boundary and None otherwise
    """
    if (num := elements[i]) > boundary:
        return num
    return None
