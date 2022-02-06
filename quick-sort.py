from typing import List


def quicksort(nums: List[int]):
    sort(nums, 0, len(nums) - 1)


def pickpivot(left: int, right: int) -> int:
    return left


def sort1(nums: List[int], left: int, right: int):
    if left >= right:
        return
    p = pickpivot(left, right)
    pivot = nums[p]
    nums[left], nums[p] = nums[p], nums[left]
    i = left + 1
    j = i
    while j <= right:
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
        j += 1

    np = i - 1
    nums[left], nums[np] = nums[np], nums[left]
    sort1(nums, left, np - 1)
    sort1(nums, np + 1, right)


def sort(nums: List[int], left: int, right: int):
    if left >= right:
        return
    p = pickpivot(left, right)
    nums[left], nums[p] = nums[p], nums[left]
    i = left + 1
    j = right
    while i <= j:
        while i <= j and nums[i] <= nums[p]:
            i += 1

        while i <= j and nums[j] > nums[p]:
            j -= 1

        if i <= j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1

    np = i - 1
    nums[p], nums[np] = nums[np], nums[p]
    sort(nums, left, np - 1)
    sort(nums, np + 1, right)


if __name__ == '__main__':
    arr = [1, 5, 3, 9, 2]
    quicksort(arr)
    print(arr)
