"""
编写一个算法来判断一个数 n 是不是快乐数。
「快乐数」定义为：
对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和。
然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。
如果 可以变为  1，那么这个数就是快乐数。如果 n 是快乐数就返回 true ；不是，则返回 false 。
提示：
1 <= n <= 2^31 - 1

示例 1：
输入：19
输出：true
解释：
12 + 92 = 82
82 + 22 = 68
62 + 82 = 100
12 + 02 + 02 = 1

示例 2：
输入：n = 2
输出：false
"""


# class Solution:
#     def isHappy(self, n):
#         all_set = set()
#         while n not in all_set:
#             all_set.add(n)
#             tpm = sum(map(lambda x: int(x) ** 2, str(n)))
#             if tpm == 1:
#                 return True
#             n = tpm
#         return False


class Solution:
    def isHappy(self, n):
        all_set = set()
        while n not in all_set:
            all_set.add(n)
            tmp = 0
            while n:
                n, mod = divmod(n, 10)
                tmp += mod ** 2
            if tmp == 1:
                return True
            n = tmp
        return False


n = 19
# n = 2
print(Solution().isHappy(n))
