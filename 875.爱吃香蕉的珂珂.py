"""
题目：
珂珂喜欢吃香蕉。这里有N堆香蕉，第 i 堆中有piles[i]根香蕉。警卫已经离开了，将在H小时后回来。
珂珂可以决定她吃香蕉的速度K(单位：根/小时)。每个小时，她将会选择一堆香蕉，从中吃掉 K 根。如果这堆香蕉少于 K 根，她将吃掉这堆的所有香蕉，然后这一小时内不会再吃更多的香蕉。
珂珂喜欢慢慢吃，但仍然想在警卫回来前吃掉所有的香蕉。
返回她可以在 H 小时内吃掉所有香蕉的最小速度 K(K 为整数)。

示例：
示例 1：
输入: piles = [3,6,7,11], H = 8
输出: 4

示例2：
输入: piles = [30,11,23,4,20], H = 5
输出: 30

示例3：
输入: piles = [30,11,23,4,20], H = 6
输出: 23
"""


class Solution:
    def minEatingSpeed(self, piles, h):
        def cost(k):
            t = 0
            for i in piles:
                t += (i + k - 1) // k
            return t

        left, right = 1, max(piles)
        while left < right:
            mid = (left + right) // 2
            ret = cost(mid)
            if ret <= h:
                right = mid
            else:
                left = mid + 1
        return left

piles = [30,11,23,4,20]
h = 6
print(Solution().minEatingSpeed(piles, h))