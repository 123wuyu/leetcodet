'''
给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a ，b ，c ，使得 a + b + c = 0 ？
请找出所有和为 0 且 不重复 的三元组。
提示：
0 <= nums.length <= 3000
-10 ^ 5 <= nums[i] <= 10 ^ 5

示例 1：
输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
示例 2：
输入：nums = []
输出：[]
示例 3：
输入：nums = [0]
输出：[]
'''

nums = [-1, 0, 1, 2, -1, -4]


class Solution:
    def threeSum(self, nums):
        nums.sort()  # [-4, -1, -1, 0, 1, 2]
        ret = []
        for i in range(len(nums) - 2):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left = i + 1
            right = len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total == 0:
                    ret.append([nums[i], nums[left], nums[right]])
                    a = nums[left]
                    while left < right and nums[left] == a:
                        left += 1
                elif total > 0:
                    right -= 1
                else:
                    left += 1
        return ret


print(Solution().threeSum(nums))
