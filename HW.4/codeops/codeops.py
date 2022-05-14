import types
import dis
from collections import deque, Counter


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    deq: deque[types.CodeType] = deque()
    deq.append(source_code)
    a = []
    while deq:
        for op in dis.get_instructions(deq.popleft()):
            a.append(op.opname)
            if isinstance(op.argval, types.CodeType):
                deq.append(op.argval)
    return Counter(a)
