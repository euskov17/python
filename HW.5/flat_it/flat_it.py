from typing import Iterable, Generator, Any


def flat_it(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    for i in sequence:
        if isinstance(i, Iterable) and len(list(i)) > 1:
            yield from flat_it(i)
        else:
            yield i
