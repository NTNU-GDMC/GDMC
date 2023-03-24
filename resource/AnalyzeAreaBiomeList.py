from gdpc import WorldSlice


def getAllBiomeList(WORLDSLICE: WorldSlice, settlementArea):
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    biome = []
    x, y = len(settlementArea), len(settlementArea[0])
    # 01 Map to coord of (x, z)
    for i in range(1, x):
        for j in range(1, y):
            if (settlementArea[i][j] == 1):
                # print("(x, y) = (", i, ", ", j, ")")
                biome.append(WORLDSLICE.getBiome((i, int(heights[(i, j)]), j)))
    biome = list(set(biome))
    return biome
