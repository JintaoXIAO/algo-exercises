from typing import List
from random import randint


def randomselect(nums: List[int], n: int) -> int:
    assert 0 < n < len(nums)
    return _randomselect(nums, 0, len(nums) - 1, n - 1)


def _partition(nums: List[int], start: int, end: int) -> int:
    p = start + randint(start, end)
    nums[start], nums[p] = nums[p], nums[start]
    i = start + 1
    j = i
    pivot = nums[start]
    while j <= end:
        if nums[j] < pivot:
            nums[j], nums[i] = nums[i], nums[j]
            i += 1
        j += 1

    nums[i - 1], nums[start] = nums[start], nums[i - 1]
    return i - 1


def _randomselect(nums: List[int], start: int, end: int, idx: int) -> int:
    if start == end:
        return nums[start]
    if start > end:
        return -1
    p = _partition(nums, start, end)
    if idx == p:
        return nums[p]
    elif p > idx:
        return _randomselect(nums, start, p - 1, idx)
    else:
        return _randomselect(nums, p + 1, end,  idx - p - 1)


if __name__ == '__main__':
    r = randomselect([9, 5, 7, 1, 10, 2, 3], 1)
    print(r)
