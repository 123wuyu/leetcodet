'''
给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。
提示：
0 <= s.length <= 5 * 10 ^ 4
s 由英文字母、数字、符号和空格组成
示例1:
输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

示例 2:
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1
'''

# s = "abcabcbb"  # 3
s = "bbbbb" # 1


class Solution:
    def longestSubStr(self, s):
        dict = {}
        left = 0
        ret = 0
        for i, j in enumerate(s):
            if j in dict:
                left = max(left, dict[j] + 1)
            dict[j] = i
            ret = max(ret, i - left + 1)
        return ret


print(Solution().longestSubStr(s))
