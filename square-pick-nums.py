from typing import List, Tuple


def _process(n: int, tab: List[List[int]]):
    for x in range(n):
        for y in range(n):
            v1 = tab[x - 1][y] if x > 0 else 0
            v2 = tab[x][y - 1] if y > 0 else 0
            if v1 > v2:
                tab[x][y] += v1
                if x > 0:
                    tab[x - 1][y] = 0
            else:
                tab[x][y] += v2
                if y > 0:
                    tab[x][y - 1] = 0


def _init(n: int, vs: List[Tuple[int, int, int]]) -> List[List[int]]:
    tab = [[0 for _ in range(n)] for _ in range(n)]
    for v in vs:
        tab[v[0]][v[1]] = v[2]
    return tab


def solve(N, vs):
    tab = _init(N, vs)
    _process(N, tab)
    _process(N, tab)
    print(tab[N - 1][N - 1])


if __name__ == '__main__':
    N = int(input())
    vs = []
    try:
        while True:
            x, y, v = map(int, input().split())
            vs.append((x, y, v))
    except EOFError:
        pass
    solve(N, vs)
