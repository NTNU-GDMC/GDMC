"""
README:
!!! DO NOT DELETE THESE ANNOTATION !!!
    nbtName       # building name
    level         # 1 ~ 3
    position      # init for (0, 0, 0)
    doorPos       # take this from data/structure/<xxx>.json | or your Entry.py file
    length        # take this from data/structure/<xxx>.json
    width         # take this from data/structure/<xxx>.json
    materialType  # take this from data/structure/<xxx>.json, 
    !!! Be careful that the material type in json file is default type, you can change it, anyway, after initial Building class !!!

!!! "building material" -> "biome" Table !!!
    current
        "oak"         -> grass plain biome
        "spruce"      -> snow biome
        "sand"        -> desert biome
    backlog
        "jungle"      -> forest biome
        "mangrove"    -> mangrove biome
        "ice"         -> frozen biome
        "red_sand"    -> bad land biome
"""

from gdpc.vector_tools import dropY, ivec2, ivec3
from ..building.building_info import BuildingInfo


class Building:
    def __init__(self, building_info: BuildingInfo, position: ivec2, level: int = 1):
        self.id: int | None = None
        self.building_info = building_info
        self.level = level
        self.position = position
        self._material = "oak"

    @property
    def type(self):
        return self.building_info.type

    @property
    def maxSize(self):
        return self.building_info.max_size

    @property
    def currentSize(self):
        return self.building_info.structures[self.level-1].size

    @property
    def entryPos(self) -> ivec2 | None:
        entries = self.building_info.structures[self.building_info.maxLevel-1].entries
        if len(entries) == 0:
            return None
        pos = entries[0].pos
        return self.position + dropY(pos)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, name: str):
        self._material = name
