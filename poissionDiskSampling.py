from math import sqrt, floor, pi, sin, cos, dist, abs
from random import random, randint


def terrainRelief(sx,sz,ex,ez,heights,threshold):
    avg = 0
    for x in range(sx,ex):
        for z in range(sz,ez):
            avg += heights[x][z]

    avg = avg // (ex - sx) * (ez - sz)
    diff = 0 
    for x in range(sx,ex):
        for z in range(sz,ez):
            diff += abs(heights[x][z] - avg)
    
    return diff <= threshold

def poissionSample(sx, sy, ex, ey, num, minRange,acceptPos,heights) -> list:
    k = 30  # sample number
    if sx > ex:
        sx, ex = ex, sx
    if sy > ey:
        sy, ey = ey, sy
    acceptPositionSet = set(acceptPos)
    w = minRange / sqrt(2)
    xlen = ex - sx
    ylen = ey - sy
    cols = floor(xlen / w) + 1
    rows = floor(ylen / w) + 1

    cells = [[-1 for i in range(cols)] for i in range(rows)]
    activeList = []
    randChunk = acceptPos[randint(0,len(acceptPos) - 1)]
    pos = [ randChunk[0] +randint(0,16) - sx, randChunk[1] + randint(0,16) - sy]
    x = floor((pos[0]-sx) / w)
    y = floor((pos[1]-sy) / w)

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
            sampleChunk = (floor(samplePoint[0] / 16) * 16,floor(samplePoint[1]  / 16) * 16)

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
                coords.append(p)
    return coords

# print(poissionSample(0,0,300,300,10,20))
