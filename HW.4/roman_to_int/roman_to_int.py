def roman_to_int(s: str) -> int:
    """
    Given a roman numeral, convert it to an integer.
    Input is guaranteed to be within the range from 1 to 3999.
    """
    roman_solo = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    roman_add = {('I', 'V'): 3, ('I', 'X'): 8, ('X', 'L'): 30, ('X', 'C'): 80, ('C', 'D'): 300, ('C', 'M'): 800}
    number = 0
    prev = None
    for symbol in s:
        if prev and roman_solo[prev] < roman_solo[symbol]:
            number += roman_add[(prev, symbol)]
        else:
            number += roman_solo[symbol]
        prev = symbol
    return number
