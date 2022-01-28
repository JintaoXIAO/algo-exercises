from typing import List, Optional

from lists import ListNode, of, printlist


class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        h = Heap(lists)
        n = h.pop()
        rst = n
        while n is not None:
            h.push(n.next)
            n.next = h.pop()
            n = n.next

        return rst

    def mergeKLists1(self, lists: List[ListNode]) -> ListNode:
        n = self.popminimum(lists)
        rst = n
        while n is not None:
            n.next = self.popminimum(lists)
            n = n.next

        return rst

    def popminimum(self, lists: List[ListNode]) -> Optional[ListNode]:
        if len(lists) == 0:
            return None

        n = -1
        for i in range(0, len(lists)):
            if lists[i] is not None:
                if n == -1 or lists[n].val > lists[i].val:
                    n = i
        if n != -1:
            rst = lists[n]
            lists[n] = lists[n].next
            return rst
        else:
            return None


class Heap:
    def __init__(self, lists: List[ListNode]):
        self.lists = []
        for node in lists:
            if node:
                self.lists.append(node)
        self._heapify()

    def __len__(self):
        return len(self.lists)

    def _heapify(self):
        size = len(self.lists)
        i = size - 1
        while i > 0:
            pi = int((i - 1) / 2)
            if self.lists[i].val < self.lists[pi].val:
                self.lists[i], self.lists[pi] = self.lists[pi], self.lists[i]
            i -= 1

    def pop(self):
        size = len(self.lists)
        if size > 0:
            head = self.lists[0]
            self.lists[0], self.lists[-1] = self.lists[-1], self.lists[0]
            self.lists.pop(size-1)
            self._heapify()
            return head
        else:
            return None

    def push(self, node: ListNode):
        if node:
            self.lists.append(node)
            self._heapify()
        else:
            pass


if __name__ == "__main__":
    l1 = of(1, 4, 5)
    l2 = of(1, 3, 4)
    l3 = of(2, 6)
    l4 = of()

    s = Solution()
    r = s.mergeKLists1([l1, l2, l3, l4])
    printlist(r)

