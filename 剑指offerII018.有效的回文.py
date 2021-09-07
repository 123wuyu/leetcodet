'''
给定一个字符串 s ，验证 s 是否是 回文串 ，只考虑字母和数字字符，可以忽略字母的大小写。
本题中，将空字符串定义为有效的 回文串 。
提示：
1 <= s.length <= 2 * 10 ^ 5
字符串 s 由 ASCII 字符组成

示例 1:
输入: s = "A man, a plan, a canal: Panama"
输出: true
解释："amanaplanacanalpanama" 是回文串

示例 2:
输入: s = "race a car"
输出: false
解释："raceacar" 不是回文串
'''

s = "A man, a plan, a canal: Panama"  # True


# class Solution:
#     def isPalindrome(self, s):
#         strs = ''
#         for i in s:
#             if i.isalnum():
#                 strs += i.lower()
#         return strs == strs[::-1]

class Solution:
    def isPalindrome(self, s):
        left = 0
        right = len(s) - 1
        while left <= right:
            if not s[left].isalnum():
                left += 1
            elif not s[right].isalnum():
                right -= 1
            elif s[left].lower() != s[right].lower():
                return False
            else:
                left += 1
                right -= 1
        return True



print(Solution().isPalindrome(s))
