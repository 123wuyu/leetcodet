'''
给定一个含有 n 个正整数的数组和一个正整数 target 。
找出该数组中满足其和 ≥ target 的长度最小的 连续子数组 [numsl, numsl+1, ..., numsr-1, numsr] ，
并返回其长度。如果不存在符合条件的子数组，返回 0 。
提示：
1 <= target <= 10 ^ 9
1 <= nums.length <= 10 ^ 5
1 <= nums[i] <= 10 ^ 5
示例 1：
输入：target = 7, nums = [2,3,1,2,4,3]
输出：2
解释：子数组 [4,3] 是该条件下的长度最小的子数组。

示例 2：
输入：target = 4, nums = [1,4,4]
输出：1

示例 3：
输入：target = 11, nums = [1,1,1,1,1,1,1,1]
输出：0
'''

target = 7
nums = [2, 3, 1, 2, 4, 3]


class Solution:
    def minSumList(self, target, nums):
        left = 0
        total = 0
        ret = float('inf')
        for right, num in enumerate(nums):
            total += num
            while total >= target:
                ret = min(ret, right - left + 1)
                total -= nums[left]
                left += 1
        return 0 if ret > len(nums) else ret


print(Solution().minSumList(target, nums))