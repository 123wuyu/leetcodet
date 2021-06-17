'''
题目：
给定一个循环数组(最后一个元素的下一个元素是数组的第一个元素)，输出每个元素的下一个更大元素。
数字 x 的下一个更大的元素是按数组遍历顺序，这个数字之后的第一个比它更大的数，这意味着你应该循环地搜索它的
下一个更大的数。如果不存在，则输出 -1。

注意: 输入数组的长度不会超过 10000。
输入: [1,2,1]
输出: [2,-1,2]
解释: 第一个 1 的下一个更大的数是 2；
数字 2 找不到下一个更大的数；
第二个 1 的下一个最大的数需要循环搜索，结果也是 2
'''


# class Solution:
#     def nextGreaterElements(self, nums):
#         ln = len(nums)
#         ret = [-1] * ln
#         point = 0
#         while point < ln:
#             for i in range(point + 1, 2 * ln):
#                 if nums[i % ln] > nums[point]:
#                     ret[point] = nums[i % ln]
#                     break
#             point += 1
#         return ret

# class Solution:
#     def nextGreaterElements(self, nums):
#         ln = len(nums)
#         ret = [-1] * ln
#         stack = []
#         for i in range(ln*2-1):
#             while stack and nums[stack[-1]] < nums[i%ln]:
#                 ret[stack.pop()] = nums[i%ln]
#             stack.append(i%ln)
#         return ret

class Solution:
    def nextGreaterElements(self, nums):
        ln = len(nums)
        ret = [-1] * ln
        stack = []
        for index, num in enumerate(nums):
            while stack and nums[stack[-1]] < num:
                ret[stack.pop()] = num
            stack.append(index)

        ind = 0
        while stack and ind < ln:
            while stack and nums[stack[-1]] < nums[ind]:
               ret[stack.pop()] = nums[ind]
            ind += 1
        return ret

nums = [1, 2, 1]
print(Solution().nextGreaterElements(nums))