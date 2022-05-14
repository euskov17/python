import typing as tp


def find_median(nums1: tp.Sequence[int], nums2: tp.Sequence[int]) -> float:
    """
    Find median of two sorted sequences.
    At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    if (len1 := len(nums1)) == 0:
        return (nums2[len(nums2) // 2] +
                nums2[len(nums2) // 2 - 1 + len(nums2) % 2]) / 2
    if (len2 := len(nums2)) == 0:
        return (nums1[len1 // 2] + nums1[len1 // 2 - 1 + len1 % 2]) / 2
    el_taken1 = 0
    el_taken2 = 0
    length = len1 + len2
    middle = length // 2 + length % 2
    while el_taken1 + el_taken2 < middle:
        if el_taken1 >= len1 \
           or (el_taken2 < len2 and nums1[el_taken1] > nums2[el_taken2]):
            el_taken2 += 1
        else:
            el_taken1 += 1
    print('it_1 = ', el_taken1, end='\n')
    print('it_2 = ', el_taken2, end='\n')
    if length % 2 == 1:
        if el_taken1 == 0:
            return float(nums2[el_taken2 - 1])
        if el_taken2 == 0:
            return float(nums1[el_taken1 - 1])
        return float(max(nums2[el_taken2 - 1], nums1[el_taken1 - 1]))
    else:
        if el_taken1 == 0:
            if el_taken2 == len2:
                return (nums2[el_taken2 - 1] +
                        nums1[max(el_taken1 - 1, 0)]) / 2
            return (nums2[el_taken2 - 1] +
                    min(nums2[el_taken2], nums1[max(el_taken1 - 1, 0)]))/2
        if el_taken2 == 0:
            if el_taken1 == len1:
                return (nums1[el_taken1 - 1] +
                        nums2[max(el_taken2 - 1, 0)]) / 2
            return (nums1[el_taken1 - 1] +
                    min(nums1[el_taken1], nums2[max(el_taken2 - 1, 0)])) / 2
        if nums1[el_taken1 - 1] < nums2[el_taken2 - 1]:
            if el_taken2 == len2:
                return (nums2[el_taken2 - 1] + nums1[el_taken1]) / 2
            if el_taken1 == len1:
                return (nums2[el_taken2 - 1] + nums2[el_taken2])/2
            else:
                return (nums2[el_taken2 - 1] +
                        min(nums2[el_taken2], nums1[el_taken1])) / 2
        else:
            if el_taken1 == len1:
                return (nums1[el_taken1 - 1] + nums2[el_taken2]) / 2
            if el_taken2 == len2:
                return (nums1[el_taken1 - 1] + nums1[el_taken1]) / 2
            else:
                return (nums1[el_taken1 - 1] +
                        min(nums1[el_taken1], nums2[el_taken2])) / 2
