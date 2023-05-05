from gdpc import WorldSlice
from gdpc.vector_tools import Box


def getAllBiomeList(WORLDSLICE: WorldSlice, settlementArea: Box):
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    biome = []
    x, _, z = settlementArea.size
    # 01 Map to coord of (x, z)
    for i in range(0, x):
        for j in range(0, z):
            #  TODO: check if settlement or not _ SubaRya
            a, _, c = settlementArea.offset
            biome.append(WORLDSLICE.getBiome(
                (i + a, int(heights[(i + a, j + c)]), j + c)))
    biome = list(set(biome))
    return biome
