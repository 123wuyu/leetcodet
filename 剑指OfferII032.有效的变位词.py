'''
给定两个字符串 s 和 t ，编写一个函数来判断它们是不是一组变位词(字母异位词)。
注意：若 s 和 t 中每个字符出现的次数都相同且字符顺序不完全相同，则称 s 和 t 互为变位词(字母异位词)。
提示:
1 <= s.length, t.length <= 5 * 10 ^ 4
s and t 仅包含小写字母

示例 1:
输入: s = "anagram", t = "nagaram"
输出: true

示例 2:
输入: s = "rat", t = "car"
输出: false

示例 3:
输入: s = "a", t = "a"
输出: false
'''

s = "anagram"
t = "nagaram"  # 输出: true

# class Solution:
#     def isAnagram(self, s: str, t: str) -> bool:
#         if len(s) != len(t) or s == t:
#             return False
#         comp = [0] * 26
#         for i in s:
#             index = ord(i) - ord('a')
#             comp[index] += 1
#         for j in t:
#             index = ord(j) - ord('a')
#             if comp[index] < 1:
#                 return False
#             comp[index] -= 1
#         return True

from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return s != t and Counter(s) == Counter(t)


print(Solution().isAnagram(s, t))