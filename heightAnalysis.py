import queue
import random

def parseHeight(heights : [][]):
    mx = (len(heights) // 16) * 16 
    my = (len(heights[0]) // 16) * 16 
    res = [[0 for i in range(my)] * mx]
    for x in range(0,mx,16):
        for y in range(0,my,16):
            h = 0
            for i in range(x):
                for j in range(j):
                    h = h + heights[i][j]
            h = h // 256
            res[x//16][y//16] = h

    return res
            
def getSmoothChunk(heights : [][]): # input is 2 2d array of blocks height
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
    
    vis = [[False] * m] * n

    q = queue.Queue()
    dx = [1,-1,0,0]
    dy = [0,0,1,-1]
    resCnt = 0
    resX = -1
    resY = -1
    for x in range(n):
        for y in range(m):
            cnt = 1
            q.put([x,y])
            while not q.empty():
                cur = q.get()
                cx = cur[0]
                cy = cur[1]
                if vis[cx][cy]:
                    continue
                vis[cx][cy] True
                for i in range(4):
                    nx = x + dx[i]
                    ny = y + dy[i]
                    if nx < 0 or ny < 0 or nx == x or ny == y:
                        continue
                    if abs(chunks[cx][cy] - chunks[nx][ny]) > 1:
                        continue
                    q.put([nx,ny])
                    cnt = cnt + 1

        
        if resCnt < cnt:
            resX = x
            resY = y
            resCnt = cnt

    vis = [[False] * m] * n
    res = [[resX,resY]]
    q.put([resX,resY])
    while not q.empty():
        cur = q.get()
        cx = cur[0]
        cy = cur[1]
        if vis[cx][cy]:
            continue
        vis[cx][cy] True
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or ny < 0 or nx == x or ny == y:
                continue
            if abs(chunks[cx][cy] - chunks[nx][ny]) > 1:
                continue
            q.put([nx,ny])
            res.append([nx,ny])
         
    return res # return the list of smooth chunks indices















