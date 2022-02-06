from typing import List


def median1(arr: List[int]) -> float:
    m = 0
    l = len(arr)
    while m < l / 2:
        m += 1

    if 2 * m == l:
        return (arr[m] + arr[m - 1]) / 2
    else:
        return arr[m]


def median2(arr1: List[int], arr2: List[int]) -> float:
    l1 = len(arr1)
    l2 = len(arr2)
    m1 = 0
    m2 = 0
    while m1 + m2 < (l1 + l2) // 2:
        if m1 == l1:
            m2 = (l1 + l2) // 2 - m1
        elif m2 == l2:
            m1 = (l1 + l2) // 2 - m2
        else:
            if arr1[m1] < arr2[m2]:
                m1 += 1
            elif arr1[m1] > arr2[m2]:
                m2 += 1
            else:
                m1 += 1
                m2 += 1

    if 2 * (m1 + m2) == l1 + l2:
        if m1 == l1:
            if m2 > 0:
                return (arr2[m2] + max(arr2[m2 - 1], arr1[m1 - 1])) / 2
            else:
                return (arr2[m2] + arr1[m1 - 1]) / 2
        elif m2 == l2:
            if m1 > 0:
                return (arr1[m1] + max(arr1[m1 - 1], arr2[m2 - 1])) / 2
            else:
                return (arr1[m1] + arr2[m2 - 1]) / 2
        else:
            return (max(arr1[m1 - 1], arr2[m2 - 1]) + min(arr1[m1], arr2[m2])) / 2
    else:
        # odd total length
        # 2 * (m1 + m2) == l1 + l2 + 1
        if m1 == l1:
            return arr2[m2]
        elif m2 == l2:
            return arr1[m1]
        else:
            return min(arr1[m1], arr2[m2])


if __name__ == '__main__':
    nums1 = list(map(int, input().split()))
    nums2 = list(map(int, input().split()))

    print(median2(nums1, nums2))
