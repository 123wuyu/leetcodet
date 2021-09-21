s = "(()())(())"  # 输出："()()()"


class Solution:
    def removeOuterParentheses(self, s):
        ret = ""
        stack = []
        for i in range(len(s)):
            if s[i] == '(':
                stack.append(i)
            else:
                left = stack.pop()
                if not stack:
                    ret += s[left + 1:i]
        return ret


print(Solution().removeOuterParentheses(s))
