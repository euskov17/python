import typing as tp
import heapq


def merge(input_streams: tp.Sequence[tp.IO[bytes]],
          output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams.
    Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream.
    Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    seq = [list(map(int, list(filter(None, inp.read().decode().split('\n')))))
           for inp in input_streams]
    for el in seq:
        el.sort()
    heap = []
    for i in range(len(seq)):
        if seq[i]:
            heap.append((seq[i][0], i, 0))
    heapq.heapify(heap)
    result = []
    while heap:
        extract_min = heapq.heappop(heap)
        result.append(extract_min[0])
        index_of_list = extract_min[1]
        index_in_list = extract_min[2]
        if len(seq[index_of_list]) > index_in_list + 1:
            heapq.heappush(heap, (seq[index_of_list][index_in_list + 1],
                                  index_of_list, index_in_list + 1))
    output_stream.write(('\n'.join(list(map(str, result))) + '\n').encode())
