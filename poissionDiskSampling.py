from math import sqrt, floor, pi, sin, cos, dist
from random import random


def poissionSample(sx, sy, ex, ey, num, minRange) -> list:
    k = 30  # sample number
    if sx > ex:
        sx, ex = ex, sx
    if sy > ey:
        sy, ey = ey, sy
    # print("pS: ",sx,sy,ex,ey)
    # maxRange = 2 * minRange
    w = minRange / sqrt(2)
    xlen = ex - sx
    ylen = ey - sy
    cols = floor(xlen / w)
    rows = floor(ylen / w)
    cells = [[-1 for i in range(cols)] for i in range(rows)]
    activeList = []
    pos = [xlen * random(), ylen * random()]
    x = floor((pos[0]+sx) / w)
    y = floor((pos[1]+sy) / w)
    print(x,y,pos)
    cells[x][y] = pos
    activeList.append(pos)
    count = 0

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
            sampleX = floor(samplePoint[0] / w)
            sampleY = floor(samplePoint[1] / w)
            print(samplePoint)
            if sampleX < 0 or sampleY < 0 or sampleX >= cols or sampleY >= rows or cells[sampleX][sampleY] != -1:
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
                coords.append([p[0] + sx,p[1] + sy])


    return coords

# print(poissionSample(0,0,300,300,10,20))
