head = [1, 2, 3, 4, 5]
n = 2  # 输出：[1,2,3,5]


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        left = right = head
        count = 0
        while count < n:
            right = right.next
            count += 1
        if not right:
            return head.next
        while right.next:
            left = left.next
            right = right.next
        left.next = left.next.next
        return head


def list_to_linkedlist(alist):
    if len(alist):
        head = ListNode(alist[0])
        cur = head
        for i in range(1, len(alist)):
            cur.next = ListNode(alist[i])
            cur = cur.next
        return head

head = list_to_linkedlist(head)
print(Solution().removeNthFromEnd(head, 2))
print(head.val)
