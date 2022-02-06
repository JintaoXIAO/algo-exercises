from typing import List


def perm(cs: List[str], start: int, end: int, plst: List[str]):
    if start == end:
        plst.append(''.join(cs))
    else:
        for i in range(start, end + 1):
            cs[i], cs[start] = cs[start], cs[i]
            perm(cs, start + 1, end, plst)
            cs[i], cs[start] = cs[start], cs[i]


if __name__ == '__main__':
    s = list(input())
    plst = []
    perm(s, 0, len(s) - 1, plst)
    for p in plst:
        print(p)
