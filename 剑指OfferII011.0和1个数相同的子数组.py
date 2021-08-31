'''
给定一个二进制数组 nums , 找到含有相同数量的 0 和 1 的最长连续子数组，并返回该子数组的长度。
提示：
1 <= nums.length <= 105
nums[i] 不是 0 就是 1

示例 1:
输入: nums = [0,1]
输出: 2
说明: [0, 1] 是具有相同数量 0 和 1 的最长连续子数组。

示例 2:
输入: nums = [0,1,0]
输出: 2
说明: [0, 1] (或 [1, 0]) 是具有相同数量 0 和 1 的最长连续子数组
'''
# nums = [0,1]
nums = [0, 1, 0]  # 输出2


class Solution:
    def findMaxLength(self, nums):
        ret = pre_sum = 0
        pre_dict = {0: -1}
        # pre_dict = {}
        for index, num in enumerate(nums):
            pre_sum += -1 if num == 0 else 1
            if pre_sum in pre_dict:
                ret = max(ret, index - pre_dict[pre_sum])
            else:
                pre_dict[pre_sum] = index
        print(pre_dict)
        return ret


print(Solution().findMaxLength(nums))
