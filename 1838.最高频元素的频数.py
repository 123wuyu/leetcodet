'''
元素的 频数 是该元素在一个数组中出现的次数。
给你一个整数数组 nums 和一个整数 k 。在一步操作中，你可以选择 nums 的一个下标，并将该下标对应元素的值增加 1 。
执行最多 k 次操作后，返回数组中最高频元素的 最大可能频数 。
提示：
1 <= nums.length <= 10^5
1 <= nums[i] <= 10^5
1 <= k <= 10^5

示例 1：
输入：nums = [1,2,4], k = 5
输出：3
'''
from typing import List


class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        nums.sort()
        left, right, pre_sum, ret = 0, 1, 0, 1
        while right < len(nums):
            pre_sum += (right - left) * (nums[right] - nums[right - 1])
            while pre_sum > k:
                pre_sum -= nums[right] - nums[left]
                left += 1
            ret = max(ret, right - left + 1)
            right += 1
        return ret


nums = [1, 2, 4]
k = 5
print(Solution().maxFrequency(nums, k))
