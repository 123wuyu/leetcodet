'''
给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，
返回它将会被按顺序插入的位置.你可以假设数组中无重复元素。
输入: [1,3,5,6], 7
输出: 4
'''


class Solution:
    def searchInsert(self, nums, target):
        left, right = 0, len(nums) -1
        while left <= right:
            mid = (left + right) //2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            elif nums[mid] > target:
                right = mid - 1
        return left


nums = [1, 3, 5, 6]
target = 7

print(Solution().searchInsert(nums, target))
