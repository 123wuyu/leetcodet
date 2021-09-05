'''
给定两个字符串 s1 和 s2，写一个函数来判断 s2 是否包含 s1 的某个变位词。
换句话说，第一个字符串的排列之一是第二个字符串的 子串 。
提示：
1 <= s1.length, s2.length <= 10^4
s1 和 s2 仅包含小写字母
示例 1：
输入: s1 = "ab" s2 = "eidbaooo"
输出: True
解释: s2 包含 s1 的排列之一 ("ba").
示例 2：
输入: s1= "ab" s2 = "eidboaoo"
输出: False

'''
s1 = "ab"
s2 = "dbao"


class Solution:
    @classmethod
    def checkInclusion(cls, s1: str, s2: str) -> bool:
        arr1, arr2 = [0] * 26, [0] * 26
        if len(s1) > len(s2):
            return False

        for i in range(len(s1)): # 2
            arr1[ord(s1[i]) - ord('a')] += 1
            arr2[ord(s2[i]) - ord('a')] += 1

        for j in range(len(s1), len(s2)): #   range(2,4)
            if arr1 == arr2:
                print(222222222222222222)
                print(arr1)
                print(arr2)
                return True
            arr2[ord(s2[j - len(s1)]) - ord('a')] -= 1
            arr2[ord(s2[j]) - ord('a')] += 1

        return arr1 == arr2


print(Solution.checkInclusion(s1, s2))
