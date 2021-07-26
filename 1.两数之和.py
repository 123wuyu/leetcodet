'''
题目：
给定一个整数数组 nums和一个整数目标值 target，请你在该数组中找出 和为目标值 的那两个整数，并返回它们的数组下标。
你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。
你可以按任意顺序返回答案。

示例 1： 输入：nums = [2,7,11,15], target = 9 输出：[0,1] 解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
示例 2： 输入：nums = [3,2,4], target = 6 输出：[1,2]
示例 3： 输入：nums = [3,3], target = 6 输出：[0,1]
提示： 2 <= nums.length <= 103 -109 <= nums[i] <= 109 -109 <= target <= 109 只会存在一个有效答案
'''


# class Solution:
#     def twoSum(self, nums, target):
#         for i in range(len(nums) - 1):
#             for j in range(i + 1, len(nums)):
#                 if nums[i] + nums[j] == target:
#                     return [i, j]

class Solution:
    def twoSum(self, nums, target):
        for i in range(len(nums) - 1):
            other = target - nums[i]
            if other in nums[i+1:]:
                # return [i, nums.index(other)]
                return [i, nums.index(other, i + 1)]


# class Solution:
#     def twoSum(self, nums, target):
#         tmp = {}
#         for k, v in enumerate(nums):
#             if target - nums[k] in tmp:
#                 return [tmp[target - nums[k]], k]
#             tmp[v] = k


# nums = [2, 7, 11, 15]
# target = 9
nums = [3, 2, 4]
target = 6  # 输出：[1,2]
print(Solution().twoSum(nums, target))
