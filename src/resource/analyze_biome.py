import numpy as np
from dataclasses import dataclass
from collections import Counter
from gdpc import WorldSlice
from gdpc.vector_tools import Box, Rect
from .biome_substitute import spruceSet, birchSet, jungleSet, acaciaSet, darkOakSet, desertSet, redSandSet, otherSet


@dataclass
class BiomeMap():
    biomes: dict[tuple[int, int], str]
    cold: np.ndarray
    forest: np.ndarray
    jungle: np.ndarray
    savanna: np.ndarray
    darkForest: np.ndarray
    desert: np.ndarray
    badlands: np.ndarray
    other: np.ndarray

    def __init__(self, worldSlice: WorldSlice) -> None:
        area = worldSlice.rect
        shape = area.size.to_tuple()
        heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        self.biomes = {}
        self.cold = np.zeros(shape, dtype=bool)
        self.forest = np.zeros(shape, dtype=bool)
        self.jungle = np.zeros(shape, dtype=bool)
        self.savanna = np.zeros(shape, dtype=bool)
        self.darkForest = np.zeros(shape, dtype=bool)
        self.desert = np.zeros(shape, dtype=bool)
        self.badlands = np.zeros(shape, dtype=bool)
        self.other = np.zeros(shape, dtype=bool)

        for x, z in area.inner:
            y = heights[x, z]
            biome = worldSlice.getBiome((x, y, z))
            self.biomes[(x, z)] = biome

            if biome in spruceSet:
                self.cold[x, z] = 1
            if biome in birchSet:
                self.forest[x, z] = 1
            if biome in jungleSet:
                self.jungle[x, z] = 1
            if biome in acaciaSet:
                self.savanna[x, z] = 1
            if biome in darkOakSet:
                self.darkForest[x, z] = 1
            if biome in desertSet:
                self.desert[x, z] = 1
            if biome in redSandSet:
                self.badlands[x, z] = 1
            if biome in otherSet:
                self.other[x, z] = 1

    def getPrimaryBiome(self, area: Rect):
        """Get the primary biome in the area"""

        biomesCount: Counter[str] = Counter()

        for x, z in area.inner:
            if (x, z) in self.biomes:
                biomesCount[self.biomes[(x, z)]] += 1

        # get 1 most, get index at 0, get key at 0
        return biomesCount.most_common(1)[0][0]


def getAllBiomeList(WORLDSLICE: WorldSlice, settlementArea: Box):
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    biome = set()
    x, _, z = settlementArea.size
    # 01 Map to coord of (x, z)
    for i in range(0, x):
        for j in range(0, z):
            #  TODO: check if settlement or not _ SubaRya
            a, _, c = settlementArea.offset
            biome.add(WORLDSLICE.getBiome(
                (i + a, int(heights[(i + a, j + c)]), j + c)))
    biome = list(biome)
    return biome
