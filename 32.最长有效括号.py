"""
给你一个只包含 '(' 和 ')' 的字符串，找出最长有效(格式正确且连续)括号子串的长度。
提示：
0 <= s.length <= 3 * 10 ^ 4
s[i] 为 '(' 或 ')'

输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"
"""


class Solution:
    @staticmethod
    def longestValidParentheses(s: str) -> int:
        lg = len(s)
        nums = [i for i in range(lg) if s[i] == '(']  # [1, 3]
        if len(nums) == lg:
            return 0
        ret = 0
        for left in nums:
            a, b = 0, 0
            for i in range(left, lg):
                if s[i] == '(':
                    a += 1
                else:
                    b += 1
                if a == b:
                    ret = max(ret, a * 2)
                elif b > a:
                    break
        return ret


s = ")()())"
print(Solution.longestValidParentheses(s))
