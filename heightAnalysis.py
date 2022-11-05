import queue
import random

def parseHeight(heights : []):
    mx = (len(heights) // 16) 
    my = (len(heights[0]) // 16) 
    res = [[0 for i in range(my)] for i in range(mx)]
    for x in range(mx):
        for y in range(my):
            h = 0
            for i in range(x*16,x*16 + 16):
                for j in range(y*16,y*16 + 16):
                    h = h + heights[i][j]
            h = h // 256
            res[x][y] = h

    return res
            
def getSmoothChunk(heights : []): # input is a 2d array of blocks height
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
    dx = [1,-1,0,0]
    dy = [0,0,1,-1]
    resCnt = 0
    resX = -1
    resY = -1

    for arr in chunks:
        print(arr)
    for x in range(1):
        for y in range(1):
            vis = [[False] * m] * n
            cnt = 1
            q.put([x,y])
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
                    print(nx,ny)
                    if nx < 0 or ny < 0 or nx == n or ny == m:
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
        vis[cx][cy] = True
        for i in range(4):
            nx = cx + dx[i]
            ny = cy + dy[i]
            if nx < 0 or ny < 0 or nx == n or ny == m:
                continue
            if abs(chunks[cx][cy] - chunks[nx][ny]) > 1:
                continue
            q.put([nx,ny])
            res.append([nx* 16,ny * 16])
         
    return res # return the list of smooth chunks,corner location (offset to 0,0)















