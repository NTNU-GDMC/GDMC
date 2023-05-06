import queue
import random


def parseHeight(heights: list[list[int]]):
    mx = (len(heights) // 16)
    my = (len(heights[0]) // 16)
    res = [[0 for i in range(my)] for i in range(mx)]
    for x in range(mx):
        for y in range(my):
            h = 0
            for i in range(x * 16, x * 16 + 16):
                for j in range(y * 16, y * 16 + 16):
                    h = h + heights[i][j]
            h = h // 256
            res[x][y] = h
    print("chunk height average:")
    for arr in res:
        print(arr)
    print()
    return res


# input is a 2d array of blocks height
def getSmoothChunk(heights: list[list[int]]):
    """
        analysis:
            use any chuck as center and bfs, only adds the neighbor to the queue
            when the level difference is less then 2
    """
    chunks = parseHeight(heights)

    n = len(chunks)
    if n == 0:
        return []
    m = len(chunks[0])

    q = queue.Queue()
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    resCnt = 0
    resX = -1
    resY = -1

    for x in range(n):
        for y in range(m):
            vis = [[False for i in range(m)] for i in range(n)]
            cnt = 1
            q.put([x, y])
            while not q.empty():
                cur = q.get()
                cx = cur[0]
                cy = cur[1]
                if vis[cx][cy]:
                    continue
                vis[cx][cy] = True
                for i in range(4):
                    nx = cx + dx[i]
                    ny = cy + dy[i]
                    if nx < 0 or ny < 0 or nx == n or ny == m:
                        continue
                    if abs(chunks[cx][cy] - chunks[nx][ny]) > 2:
                        continue
                    q.put([nx, ny])

                    cnt = cnt + 1

            if resCnt < cnt:
                resX = x
                resY = y
                resCnt = cnt

    vis = [[False for i in range(m)] for i in range(n)]

    res = []
    q.put([resX, resY])

    print(resCnt)
    while not q.empty():
        cur = q.get()
        print(cur)
        cx = cur[0]
        cy = cur[1]
        if vis[cx][cy]:
            print(cur, " visited")
            continue
        else:
            print(cur, " not visited")

        vis[cx][cy] = True
        for arr in vis:
            print(arr)
        print()
        print("append ", (cx, cy))
        res.append((cx * 16, cy * 16))
        for i in range(4):
            nx = cx + dx[i]
            ny = cy + dy[i]
            if nx < 0 or ny < 0 or nx == n or ny == m:
                continue

            if abs(chunks[cx][cy] - chunks[nx][ny]) <= 2:
                q.put([nx, ny])
                print("put ", [nx, ny])

    print("analysis done")
    print(res)
    # return the list of smooth chunks,corner location (offset to 0,0)
    return res


def getAvailableBuildArea(heights: list[list[int]]):
    """
        analysis:
            use any chuck as center and bfs, only adds the neighbor to the queue
            when the level difference is less then 2
    """
    chunks = parseHeight(heights)

    n = len(chunks)
    if n == 0:
        return []
    m = len(chunks[0])

    q = queue.Queue()
    dx = [1, -1, 0, 0]
    dy = [0, 0, 1, -1]
    resCnt = 0
    resX = -1
    resY = -1

    for x in range(n):
        for y in range(m):
            vis = [[False for i in range(m)] for i in range(n)]
            cnt = 1
            q.put([x, y])
            while not q.empty():
                cur = q.get()
                cx = cur[0]
                cy = cur[1]
                if vis[cx][cy]:
                    continue
                vis[cx][cy] = True
                for i in range(4):
                    nx = cx + dx[i]
                    ny = cy + dy[i]
                    if nx < 0 or ny < 0 or nx == n or ny == m:
                        continue
                    if abs(chunks[cx][cy] - chunks[nx][ny]) > 2:
                        continue
                    q.put([nx, ny])

                    cnt = cnt + 1

            if resCnt < cnt:
                resX = x
                resY = y
                resCnt = cnt

    vis = [[False for i in range(m)] for i in range(n)]

    q.put([resX, resY])

    res = [[0 for i in range(len(heights[0]))] for i in range(len(heights))]
    while not q.empty():
        cur = q.get()
        cx = cur[0]
        cy = cur[1]
        if vis[cx][cy]:
            continue
        vis[cx][cy] = True
        if (q.qsize() > 10000):
            for a in vis:
                print(a)
            return []
        for curX in range(cx * 16, cx * 16 + 16):
            for curY in range(cy * 16, cy * 16 + 16):
                res[curX][curY] = 1
        for i in range(0, 4):
            nx = cx + dx[i]
            ny = cy + dy[i]
            if nx < 0 or ny < 0 or nx == n or ny == m:
                continue
            if abs(chunks[cx][cy] - chunks[nx][ny]) <= 2:
                q.put([nx, ny])

    # return a 2D array, 1 means that the position can be built.
    return res
