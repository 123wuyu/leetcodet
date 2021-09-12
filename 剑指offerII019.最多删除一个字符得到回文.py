'''
给定一个非空字符串 s，请判断如果 最多 从字符串中删除一个字符能否得到一个回文字符串。
提示:
1 <= s.length <= 10 ^ 5
s 由小写英文字母组成

示例 1:
输入: s = "aba"
输出: true

示例 2:
输入: s = "abca"
输出: true
解释: 可以删除 "c" 字符 或者 "b" 字符

示例 3:
输入: s = "abc"
输出: false
'''

s = "abca"


class Solution:
    def validPalinddrome(self, s):
        def check(l, r):
            while l <= r:
                if s[l] != s[r]:
                    break
                l += 1
                r -= 1
            return l, r

        mid = len(s) // 2
        left, right = check(0, len(s) - 1)
        if left > mid:
            return True
        return check(left + 1, right)[0] > mid or check(left, right - 1)[0] == mid


print(Solution().validPalinddrome(s))