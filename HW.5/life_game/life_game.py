class LifeGame(object):
    """
    Class for Game life
    """

    def __init__(self, m: list[list[int]]):
        self.matrix = m

    def __get_true_neighbours(self, i: int, j: int) -> list[int]:
        res = [0, 0]
        for row in range(3):
            for col in range(3):
                if row * col != 1:
                    if i + row - 1 in range(len(self.matrix)) and j + col - 1 in range(len(self.matrix[i])) and \
                            self.matrix[i + row - 1][j + col - 1] in [2, 3]:
                        res[self.matrix[i + row - 1][j + col - 1] - 2] += 1
        return res
        # for it in range(len(self.matrix[i])):
        #     if it != j and self.matrix[i][it] in [2, 3]: # and it!=j
        #         res[self.matrix[i][it] - 2] += 1
        # for it in range(len(self.matrix)):
        #     if it != i and for k in range(3):
        #     for l in range(3):
        #         if k * l != 1:
        #             if i + k - 1 in range(len(self.matrix)) and j + l - 1 in range(len(self.matrix[i])) and \
        #                     self.matrix[i + k - 1][j + l - 1] in [2, 3]:
        #                 res[self.matrix[i + k - 1][j + l - 1] - 2] += 1
        # self.matrix[it][j] in [2, 3]: # it != i
        #         res[self.matrix[it][j] - 2] += 1
        # return res

    def __next_generation_element(self, i: int, j: int) -> int:
        if self.matrix[i][j] == 1:
            return 1
        # print(i, j, self.get_true_neighbours(i, j))
        if self.matrix[i][j] in [2, 3]:
            if self.__get_true_neighbours(i, j)[self.matrix[i][j] - 2] in [2, 3]:
                return self.matrix[i][j]
            else:
                return 0
        if self.__get_true_neighbours(i, j)[0] == 3:
            return 2
        if self.__get_true_neighbours(i, j)[1] == 3:
            return 3
        return 0

    def get_next_generation(self) -> list[list[int]]:
        new_matrix = [[self.__next_generation_element(row, el) for el in range(len(self.matrix[row]))] for row in
                      range(len(self.matrix))]
        self.matrix = new_matrix
        return new_matrix
