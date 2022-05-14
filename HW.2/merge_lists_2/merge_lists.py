import typing as tp
from typing import List
import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> List[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
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
    return result
