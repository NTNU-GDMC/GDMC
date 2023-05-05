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

import os
from nbt import nbt
from ..building_util.building_info import BuildingInfo, Entry


def getJsonAbsPath(name: str, type: int, level: int) -> str:
    """
    absPath(<name>,<type>,<level>)
    Example: absPath("chalet", 1, 2) -> "...chalet1/level2.json"
    """
    return os.path.abspath(os.path.join(".", os.path.join("data", os.path.join("structures", os.path.join(name + f"{str(type)}", "level" + f"{str(level)}.json")))))


class Building():
    # TODO: 需要一個 method BuildingInfo
    # !!! @LoveSnowEx : tags had been removed
    def __init__(self, nbtName: str, type: int, level: int = 1, position: tuple[int, int] = (0, 0)):
        self.buildingInfo = BuildingInfo(getJsonAbsPath(nbtName, type, level))
        self.nbtName = nbtName              # building name
        self.level = level                  # building level: 1~3
        self.position = position            # building coord

    def getBuildingLevel(self):
        return self.level

    def getBuildingPos(self):
        return self.position

    def getBuildingInfo(self):
        return self.buildingInfo


def printNbtSize(name: str):
    """
    !!! Print NBT building size -> (x, y, z)
    """
    nbt_struct = nbt.NBTFile(os.path.join(
        os.path.join(STRUCTURE_DIR, name), f"{name}.nbt"))
    x, y, z = getStructureSizeNBT(nbt_struct)
    print(name, ":", x, y, z)


def getBuildingInfoDir(name: str):
    """
    !!! Get <building>.json file content in order to parse doorPos, length, width ... information
    """
    return os.path.join(os.path.join(STRUCTURE_DIR, name), f"{name}.json")
