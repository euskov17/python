from typing import Iterable, Sized, Iterator


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        :param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """
        self.start = 0
        self.step = 1
        if len(args) == 1:
            self.stop = args[0]
        elif len(args) == 2:
            self.stop = args[1]
            self.start = args[0]
        else:
            if args[2] == 0:
                raise ValueError
            else:
                self.stop = args[1]
                self.start = args[0]
                self.step = args[2]

    def __iter__(self) -> Iterator[int]:
        a = self.start
        b = self.stop
        mas = []
        if self.step > 0:
            while a < b:
                mas.append(a)
                a += self.step
            return iter(mas)
        else:
            while a > b:
                mas.append(a)
                a += self.step
            return iter(mas)

    def __repr__(self) -> str:
        a = 'range('
        if self.start != 0:
            a += str(self.start) + ', '
        a += str(self.stop)
        if self.step != 1:
            a += ', ' + str(self.step)
        a += ')'
        return a

    def __str__(self) -> str:
        a = 'range('
        a += str(self.start) + ', '
        a += str(self.stop)
        if self.step != 1:
            a += ', ' + str(self.step)
        a += ')'
        return a

    def __contains__(self, key: int) -> bool:
        if self.step > 0:
            return (self.stop - self.start) % self.step == 0 and self.start <= key < self.stop
        else:
            return (self.stop - self.start) % self.step == 0 and self.start >= key > self.stop

    def __getitem__(self, key: int) -> int:
        return self.start + self.step * key

    def __len__(self) -> int:
        if (dif := self.stop - self.start) * self.step >= 0:
            if dif % self.step == 0:
                return dif // self.step
            return dif // self.step + 1
        return 0
