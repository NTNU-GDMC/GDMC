from math import sqrt, floor, pi, sin, cos, dist
from random import random, randint,choice
from glm import ivec2
from gdpc.vector_tools import Integral, Rect, Vec2iLike
from collections.abc import Callable


def poissionSample(sx, sy, ex, ey, num, minRange, acceptPos) -> list:
    k = 30  # sample number
    if sx > ex:
        sx, ex = ex, sx
    if sy > ey:
        sy, ey = ey, sy
    acceptPositionSet = set(acceptPos)
    # maxRange = 2 * minRange
    w = minRange / sqrt(2)
    xlen = ex - sx
    ylen = ey - sy
    cols = floor(xlen / w) + 1
    rows = floor(ylen / w) + 1
    cells = [[-1 for i in range(cols)] for i in range(rows)]
    activeList = []
    randChunk = acceptPos[randint(0, len(acceptPos) - 1)]
    pos = [randChunk[0] + randint(0, 16) - sx,
           randChunk[1] + randint(0, 16) - sy]
    x = floor((pos[0]-sx) / w)
    y = floor((pos[1]-sy) / w)
    cells[x][y] = pos
    activeList.append(pos)
    count = 0
    print("init = ", pos)
    while len(activeList) > 0 and count < num:
        idx = floor(len(activeList) * random())
        curPos = activeList[idx]
        found = False
        for i in range(k):
            rad = 2*pi*random()
            offsetX = cos(rad)
            offsetY = sin(rad)
            mag = random() * minRange + minRange
            samplePoint = [curPos[0] + offsetX*mag, curPos[1] + offsetY*mag]
            sampleChunk = (
                floor(samplePoint[0] / 16) * 16, floor(samplePoint[1] / 16) * 16)

            sampleX = floor((samplePoint[0]) / w)
            sampleY = floor((samplePoint[1]) / w)

            if sampleX < 0 or sampleY < 0 or sampleX >= cols or sampleY >= rows or cells[sampleX][sampleY] != -1:
                continue

            if sampleChunk not in acceptPositionSet:

                continue
            flag = True
            for i in range(sampleX-1, sampleX+2):
                for j in range(sampleY-1, sampleY+2):
                    if i == sampleX and j == sampleY:
                        continue
                    if i < 0 or j < 0 or i >= cols or j >= rows:
                        continue
                    if cells[i][j] == -1:
                        continue
                    curDist = dist(cells[i][j], samplePoint)
                    if curDist < minRange:
                        flag = False
            if flag:
                cells[sampleX][sampleY] = samplePoint
                activeList.append(samplePoint)
                found = True
                count += 1
                # mycanvas.create_oval(samplePoint[0],samplePoint[1],samplePoint[0]+3,samplePoint[1]+3, fill='red')
                break

        if not found:
            del activeList[idx]
    coords = []

    for row in cells:
        for p in row:
            if p != -1:
                coords.append([p[0] + sx, p[1] + sy])

    return coords

def defaultSampleFunction(chunk: Rect) -> bool:
    return True

def poissonDiskSample(bound: Rect,limit: int, r: float,k:int = 30, sampleFunc: Callable[[Rect],bool]=defaultSampleFunction, initPoints: list[ivec2]=[]) -> list[ivec2]:
    """ 
    get the sample positions of the bound, samepleFunc is to check if the chunk can add a point
    r is the minimum distance between two points
    return a list of ivec2
    """
    [height, width] = bound.size
    [sx,sy] = bound.begin
    [ex,ey] = bound.end
    w = r / sqrt(2)
    cols = floor(height / w) + 1
    rows = floor(width / w) + 1
    activeList: list[ivec2] = []
    count = 0
    cells:list[list[int | ivec2]] = [[-1 for _ in range(cols)] for _ in range(rows)]
    pos = ivec2(sx + height * random(), sy + width *  random())

    if len(initPoints) != 0:
        pos = choice(initPoints)

    cellPos = [floor(pos[0] / w), floor(pos[1] / w)]
    cells[cellPos[0]][cellPos[1]] = pos
    
    activeList.append(pos)

    while len(activeList) > 0  and count < limit:
        idx = randint(0,len(activeList)-1)
        curPos = activeList[idx]
        found = False

        for _ in range(k):
            rad = 2 * pi * random()
            offsetX = cos(rad)
            offsetY = sin(rad)
            mag = random() * r + r
            samplePoint = ivec2(floor(curPos[0] + offsetX * mag), floor(curPos[1] + offsetY * mag))
            x,y = floor(samplePoint[0] / w), floor(samplePoint[1] / w)

            if x < 0 or y < 0 or x >= cols or y >= rows or cells[x][y] != -1:
                continue

            if not sampleFunc(Rect(offset=ivec2(x,y),size=ivec2(w,w))):
                continue
            flag = True
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i == x and j == y:
                        if i < 0 or j < 0 or i >= cols or j >= rows:
                            continue
                        if cells[i][j] == -1:
                            continue
                        curDist = dist(cells[i][j], samplePoint)
                        if curDist < r:
                            flag = False
            if flag: # found a point that works
                cells[x][y] = samplePoint
                activeList.append(samplePoint)
                found = True 
                count += 1
                break

        if not found:
            del activeList[idx]

    return []
