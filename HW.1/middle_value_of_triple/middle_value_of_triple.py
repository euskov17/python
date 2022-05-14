def get_middle_value(a: int, b: int, c: int) -> int:
    """
        Takes three values and returns middle value.
    """
    if (a-b)*(a-c) <= 0:
        return a
    if (c-b)*(c-a) <= 0:
        return c
    return b
