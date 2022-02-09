def match(s: str, i: int, p: str, j: int) -> bool:
    if j == len(p):
        return i == len(s)
    if j < len(p) and p[j] == '*':
        return match(s, i, p, j + 1) or match(s, i + 1, p, j)
    elif j < len(p):
        return i < len(s) and (s[i] == p[j] or p[j] == '?') and match(s, i + 1, p, j + 1)
    return False


def match2(s: str, p: str) -> bool:
    sl = len(s) + 1
    pl = len(p) + 1
    dp = [[False for _ in range(sl)] for _ in range(pl)]
    dp[0][0] = True
    i = 1
    while i < pl:
        j = 1
        while j < sl:
            if p[i - 1] == '*':
                dp[i][j] = dp[i - 1][j - 1] or dp[i - 1][j] or dp[i][j - 1]
            elif p[i - 1] in [s[j - 1], '?']:
                dp[i][j] = dp[i - 1][j - 1]
            j += 1
        i += 1
    return dp[-1][-1]


def ismatch(s: str, p: str) -> bool:
    return match2(s, p)


if __name__ == '__main__':
    s = input()
    p = input()
    print("'{}' is match with '{}'? {}".format(s, p, ismatch(s, p)))
