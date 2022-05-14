def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    result = ''
    for el in message:
        if ord(el) in range(ord('a'), ord('z') + 1):
            result += chr(ord('a') +
                          (ord(el) + n - ord('a')) % (ord('z') - ord('a') + 1))
        elif ord(el) in range(ord('A'), ord('Z') + 1):
            result += chr(ord('A') +
                          (ord(el) + n - ord('A')) % (ord('Z') - ord('A') + 1))
        else:
            result += el
    return result
