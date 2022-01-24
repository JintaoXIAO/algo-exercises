from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        i = 0
        l = len(nums) - 1
        while i < l:
            j = i + 1
            while j < len(nums):
                if nums[i] + nums[j] == target:
                    return [i, j]
                j += 1
            i += 1

    def twoSum1(self, nums: List[int], target: int) -> List[int]:
        m = {}
        for i in range(0, len(nums)):
            m[nums[i]] = i
        for i in range(0, len(nums)):
            if m[target - nums[i]]:
                return [i, m[target - nums[i]]]


if __name__ == '__main__':
    s = Solution()
    print(s.twoSum1([2, 7, 11, 15], 9))
    print(s.twoSum1([3, 2, 4], 6))
