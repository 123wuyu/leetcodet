'''
给一个 非空 字符串 s 和一个单词缩写 abbr ，判断这个缩写是否可以是给定单词的缩写。
字符串 "word" 的所有有效缩写为：
["word", "1ord", "w1rd", "wo1d", "wor1", "2rd", "w2d", "wo2", "1o1d", "1or1", "w1r1", "1o2", "2r1", "3d", "w3", "4"]
注意单词 "word" 的所有有效缩写仅包含以上这些。任何其他的字符串都不是 "word" 的有效缩写。
注意:
假设字符串 s 仅包含小写字母且 abbr 只包含小写字母和数字

示例 1:
给定 s = "internationalization", abbr = "i12iz4n":
函数返回 true.
 
示例 2:
给定 s = "apple", abbr = "a2e":
函数返回 false
'''''


class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        point, num, lg = 0, 0, len(word)
        for i in abbr:
            if i.isdigit():
                if num == 0 and i == '0':
                    return False
                num = num * 10 + int(i)
                continue
            if num:
                point += num
                num = 0
            if point >= lg or word[point] != i:
                return False
            point += 1
        return True if point + num == lg else False


# s = "internationalization"
# abbr = "i12iz4n"

s = "apple"
abbr = "a2e"

print(Solution().validWordAbbreviation(s, abbr))
