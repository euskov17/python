import typing as tp


def generate_matrix(n: int) -> tp.List[tp.List[int]]:
    """
    Takes integer n and returns spiral matrix with elements from 1 to n**2
    """
    matrix = [[0] * n for _ in range(n)]
    x, y = 0, 0
    x_shift = 1  # т.к начинаем обход
    y_shift = 0
    for pos in range(n ** 2):
        matrix[y][x] = pos + 1
        if x_shift:
            flag = x + x_shift
        else:
            flag = y + y_shift
        if flag < 0 or flag == n or matrix[y + y_shift][x + x_shift] != 0:
            x_shift, y_shift = -y_shift, x_shift
        x += x_shift
        y += y_shift
    return matrix
