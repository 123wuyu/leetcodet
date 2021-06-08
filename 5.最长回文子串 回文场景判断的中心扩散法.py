"""
给你一个字符串 s，找到 s 中最长的回文子串。
示例 1：
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。

示例 2：
输入：s = "cbbd"
输出："bb"

示例 3：
输入：s = "a"
输出："a"

示例 4：
输入：s = "ac"
输出："a"
"""


class Solution:
    def longestPalindrome(self, s):
        ln = len(s)
        if ln < 2:
            return s
        ret = ''

        def finder(left, right):
            nonlocal ret
            while left >= 0 and right < ln and s[left] == s[right]:
                left -= 1
                right += 1
            ret = s[left + 1:right] if right - left - 1 > len(ret) else ret

        for i in range(ln):
            finder(i, i)
            finder(i, i + 1)

        return ret


# s = "babad"
s = "cbbd"
print(Solution().longestPalindrome(s))
