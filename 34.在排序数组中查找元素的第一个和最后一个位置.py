"""
题目
给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。
如果数组中不存在目标值 target，返回 [-1, -1]。

示例 1：
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]

示例 2：
输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]

示例 3：
输入：nums = [], target = 0
输出：[-1,-1]

"""

import bisect


class Solution:
    def searchRange(self, nums, target):
        left = bisect.bisect_left(nums, target)
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        right = bisect.bisect_left(nums, target + 1)
        return [left, right - 1]


# nums = [5, 7, 7, 8, 8, 10]
# target = 8  # 输出：[3,4]
# nums = [5,7,7,8,8,10]
# target = 6    # 输出：[-1,-1]
nums = []
target = 0  # 输出：[-1,-1]
print(Solution().searchRange(nums, target))
