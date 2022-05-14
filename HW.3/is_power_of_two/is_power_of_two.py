

def is_power_of_two(n: int) -> bool:
    """
    Given a positive integer, write a function
    to find if it is a power of two or not.
    """
    if n == 1:
        return True
    if n % 2 or n < 1:
        return False
    else:
        return is_power_of_two(n // 2)
