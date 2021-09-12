'''
给定一个字符串数组 strs ，将 变位词 组合在一起。 可以按任意顺序返回结果列表。
注意：若两个字符串中每个字符出现的次数都相同，则称它们互为变位词。
提示：
1 <= strs.length <= 104
0 <= strs[i].length <= 100
strs[i] 仅包含小写字母
示例 1:
输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
示例 2:
输入: strs = [""]
输出: [[""]]
示例 3:
输入: strs = ["a"]
输出: [["a"]]
'''
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]  # [["bat"],["nat","tan"],["ate","eat","tea"]]


class Solution:
    def groupAnagrams(self, strs):
        ret = []
        d = {}
        for i in strs:
            sorted_i = ''.join(sorted(i))
            if sorted_i in d:
                ret[d[sorted_i]].append(i)
            else:
                d[sorted_i] = len(ret)
                ret.append([i])
        return ret


print(Solution().groupAnagrams(strs))