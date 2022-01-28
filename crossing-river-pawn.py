from typing import Tuple, List


def _killbyhorse(c: Tuple[int, int], h: Tuple[int, int]) -> bool:
    x, y = h
    return c in [h,
                 (x - 2, y - 1),
                 (x - 2, y + 1),
                 (x + 2, y - 1),
                 (x + 2, y + 1),
                 (x - 1, y - 2),
                 (x - 1, y + 2),
                 (x + 1, y - 2),
                 (x + 1, y + 2)]


def _helper(c: Tuple[int, int],  # current position
            b: Tuple[int, int],  # final position
            h: Tuple[int, int],  # the horse position
            visited: List[List[int]],
            path: List[Tuple[int, int]],
            paths: List[List[Tuple[int, int]]]) -> bool:
    if c == b:
        path.append(c)
        paths.append(path)
        return True
    cx, cy = c
    bx, by = b
    if cx > bx or cy > by or visited[cx][cy] or _killbyhorse(c, h):
        if cx <= bx and cy <= by:
            visited[cx][cy] = True
        return False
    path.append(c)
    p1 = _helper((cx + 1, cy), b, h, visited, path[:], paths)
    p2 = _helper((cx, cy + 1), b, h, visited, path[:], paths)
    if p1 or p2:
        return True
    visited[cx][cy] = True
    return False


def calcpath(b: Tuple[int, int], h: Tuple[int, int]) -> int:
    # start from (0,0)
    paths = []
    path = []
    s = (0, 0)
    bx, by = b
    visited: List[List[int]] = [[False for _ in range(0, by + 1)] for _ in range(0, bx + 1)]
    _helper(s, b, h, visited, path, paths)
    for p in paths:
        print(p)
    return len(paths)


def _processdp(dp: List[List[int]],
               b: Tuple[int, int],
               h: Tuple[int, int]):
    bx, by = b
    dp[1][0] = 1
    dp[0][1] = 1
    for x in range(0, bx + 1):
        for y in range(0, by + 1):
            if _killbyhorse((x, y), h):
                dp[x][y] = 0
            elif (x == 1 and y == 0) or (x == 0 and y == 1):
                pass
            else:
                p1 = (dp[x - 1][y] if x > 0 else 0)
                p2 = (dp[x][y - 1] if y > 0 else 0)
                dp[x][y] = p1 + p2


def newcalcpath(b: Tuple[int, int],
                h: Tuple[int, int]) -> int:
    bx, by = b
    dp: List[List[int]] = [[0 for _ in range(0, by + 1)] for _ in range(0, bx + 1)]
    _processdp(dp, b, h)
    return dp[bx][by]


if __name__ == '__main__':
    # px, py, hx, hy = map(lambda s: int(s), input().split(' '))
    px, py, hx, hy = 6, 6, 3, 3
    # cp = calcpath((px, py), (hx, hy))
    cp = newcalcpath((px, py), (hx, hy))
    print(cp)
