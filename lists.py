class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        return "ListNode[val={}, next=...]".format(self.val)


def of(*values):
    t = ListNode()
    p = t
    for val in values:
        n = ListNode(val)
        p.next = n
        p = p.next
    return t.next


def printlist(lst: ListNode):
    rst = ""
    p = lst
    while p.next:
        rst += "{} -> ".format(p.val)
        p = p.next
    rst += "{}".format(p.val)
    print(rst)


def fromconsole() -> ListNode:
    ins = str(input()).split(',')
    vals = map(lambda x: int(x), ins)
    return of(*vals)


if __name__ == '__main__':
    pass
