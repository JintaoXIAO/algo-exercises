if __name__ == '__main__':
    pn = int(input())
    c = [0 for _ in range(10)]
    for i in range(1, pn+1):
        for a in str(i):
            c[int(a)] += 1
    for a in c:
        print(a)
