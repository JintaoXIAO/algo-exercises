from typing import Optional

from lists import ListNode, fromconsole, printlist


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        elif not list2:
            return list1
        t = ListNode()
        l = t
        p1 = list1
        p2 = list2

        while p1 and p2:
            if p1.val < p2.val:
                l.next = p1
                p1 = p1.next
            else:
                l.next = p2
                p2 = p2.next
            l = l.next

        if p1:
            l.next = p1
        if p2:
            l.next = p2
        return t.next


if __name__ == '__main__':
    s = Solution()
    lst1 = fromconsole()
    lst2 = fromconsole()
    rst = s.mergeTwolists(lst1, lst2)
    printlist(rst)
