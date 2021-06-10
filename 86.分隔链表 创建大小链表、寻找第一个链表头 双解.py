'''
给你一个链表的头节点 head 和一个特定值 x ，请你对链表进行分隔，
使得所有 小于 x 的节点都出现在 大于或等于 x 的节点之前。
你应当 保留 两个分区中每个节点的初始相对位置。
示例 1：
输入：head = [1,4,3,2,5,2], x = 3
输出：[1,2,2,4,3,5]
示例 2：

输入：head = [2,1], x = 2
输出：[1,2]
'''


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def partition(self, head: ListNode, x: int) -> ListNode:
        if not head:
            return head
        small = ListNode()
        sm = small
        large = ListNode()
        lg = large
        while head:
            if head.val < x:
                sm.next = head
                sm = sm.next
            else:
                lg.next = head
                lg = lg.next
            head = head.next
        lg.next = None
        sm.next = large.next
        return small.next


head = [1, 4, 3, 2, 5, 2]
x = 3
print(Solution().partition(head, x))
