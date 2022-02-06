if __name__ == '__main__':
    k = int(input())
    offset = ord('a') - 1
    for _ in range(k):
        s = input()
        for c in s:
            ord(c) - offset
