'''
给定一个二进制数组 nums , 找到含有相同数量的 0 和 1 的最长连续子数组，
并返回该子数组的长度
示例 1:
输入: nums = [0,1]
输出: 2
说明: [0, 1] 是具有相同数量0和1的最长连续子数组。

示例 2:
输入: nums = [0,1,0]
输出: 2
说明: [0, 1] (或 [1, 0]) 是具有相同数量0和1的最长连续子数组。

示例 3:
输入: nums = [0,0,1,0,0,0,1,1]
输出: 6
说明: [1,0,0,0,1,1] 是具有相同数量0和1的最长连续子数组
'''

nums = [0, 0, 1, 0, 0, 0, 1, 1]  # 6


class Solution:
    def findMaxLength(self, nums):
        ret = 0
        pre_sum = 0
        dic = {0: -1}
        for i,j in enumerate(nums):
            pre_sum += 1 if j == 1 else -1
            pre_index = dic.get(pre_sum, i)
            if pre_index == i:
                dic[pre_sum] = i
            else:
                ret = max(ret, i - pre_index)
        return ret


print(Solution().findMaxLength(nums))
