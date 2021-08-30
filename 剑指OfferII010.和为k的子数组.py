'''
给定一个整数数组和一个整数 k ，请找到该数组中和为 k 的连续子数组的个数。
提示:
1 <= nums.length <= 2 * 10 ^ 4
-1000 <= nums[i] <= 1000
-10 ^ 7 <= k <= 10 ^

示例 1 :
输入:nums = [1,1,1], k = 2
输出: 2
解释: 此题 [1,1] 与 [1,1] 为两种不同的情况

示例 2 :
输入:nums = [1,2,3], k = 3
输出: 2
'''
nums = [-2, -1, 1, 2, 3]
k = 3


class Solution:
    def subarraySum(self, nums, k):
        ret = pre_sum = 0
        pre_dic = {0: 1}
        for i in nums:
            pre_sum += i
            ret += pre_dic.get(pre_sum - k, 0)
            pre_dic[pre_sum] = pre_dic.get(pre_sum, 0) + 1
        return ret


print(Solution().subarraySum(nums, k))
