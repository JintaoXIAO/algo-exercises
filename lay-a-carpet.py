if __name__ == '__main__':
    n = int(input())
    carpets = []
    for _ in range(0, n):
        x, y, w, h = map(int, input().split(' '))
        carpets.append([x, y, w, h])
    px, py = map(int, input().split(' '))
    find = False
    for i in reversed(range(n)):
        c = carpets[i]
        if c[0] <= px <= c[0] + c[2] and c[1] <= py <= c[3]:
            print(i + 1)
            find = True
            break
            
    if not find:
        print(-1)
