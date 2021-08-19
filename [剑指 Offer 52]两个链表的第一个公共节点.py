class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __eq__(self, other):
        if type(self) == type(other) and self.val == other.val:
            return True
        else:
            return False


class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        # d = {}
        # while headA:
        #     d[headA] = headA
        #     headA = headA.next
        # while headB:
        #     if d.get(headB):
        #         return headB
        #     headB = headB.next
        # return None

        x, y = headA, headB
        while x != y:
            x = x.next if x else headB
            y = y.next if y else headA
        return x


listA = [4, 1, 8, 4, 5]
listB = [5, 0, 1, 8, 4, 5]


def list_to_linkedlist(alist):
    if len(alist):
        head = ListNode(alist[0])
        cur = head
        for i in range(1, len(alist)):
            cur.next = ListNode(alist[i])
            cur = cur.next
        return head


headA = list_to_linkedlist(listA)
headB = list_to_linkedlist(listB)
print(Solution().getIntersectionNode(headA, headB).val)
