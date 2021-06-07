"""
给你一个非常大的整数 n 和一个整数数字 x ，大整数 n用一个字符串表示。n 中每一位数字和数字 x 都处于闭区间 [1, 9] 中，且 n 可能表示一个 负数 。
你打算通过在 n 的十进制表示的任意位置插入 x 来 最大化 n 的 数值 。但 不能 在负号的左边插入 x 。
例如，如果 n = 73 且 x = 6 ，那么最佳方案是将 6 插入 7 和 3 之间，使 n = 763 。如果 n = -55 且 x = 2 ，那么最佳方案是将 2 插在第一个 5 之前，使 n = -255 。返回插入操作后，用字符串表示的n 的最大值。
提示：
1 <= n.length <= 10 ** 5
1 <= x <= 9
n 中每一位的数字都在闭区间 [1, 9] 中。
n代表一个有效的整数。
当 n 表示负数时，将会以字符 '-' 开始。
"""


class Solution:
    def maxValue(self, n: str, x: int) -> str:
        start, flag, ln = 0, 1, len(n)
        if n[0] == '-':
            start, flag = 1, -1
        for i in range(start, ln):
            if x * flag > int(n[i]) * flag:
                return n[:i] + str(x) + n[i:]
        return n + str(x)


print(Solution().maxValue('73', 6))
print(Solution().maxValue('-55', 2))
