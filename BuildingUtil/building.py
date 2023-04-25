# README:
# !!! DO NOT DELETE THESE ANNOTATION !!!
    # nbtName       # building name
    # level         # 1 ~ 3
    # position      # init for (0, 0, 0)
    # doorPos       # take this from data/structure/<xxx>.json | or your Entry.py file
    # length        # take this from data/structure/<xxx>.json
    # width         # take this from data/structure/<xxx>.json
    # materialType  # take this from data/structure/<xxx>.json, 
    # !!! Be careful that the material type in json file is default type, you can change it, anyway, after initial Building class !!!

# !!! "building material" -> "biome" Table !!!
    # current
        # "oak"         -> grass plain biome
        # "spruce"      -> snow biome
        # "sand"        -> desert biome
    # backlog
        # "jungle"      -> forest biome
        # "mangrove"    -> mangrove biome
        # "ice"         -> frozen biome
        # "red_sand"    -> bad land biome

import os
from BuildingUtil.nbt_builder import getStructureSizeNBT
from nbt import nbt

STRUCTURE_DIR = os.path.abspath("./data/structures")

class Building(object):
    def __init__(self, nbtName:str, level: int, position: tuple[int, int], doorPos: tuple[int, int], length: int, width: int, offset: tuple[int, int] = (0, 0), materialType=None, tags=[]):
        self.nbtName = nbtName              # building name
        self.level = level                  # building level: 1~3
        self.position = position            # building coord
        self.doorPos = doorPos              # door coord
        self.length = length                # max length in this type of building
        self.width = width                  # max width in this type of building
        self.materialType = materialType    # building material
        # @LoveSnowEx FIXME: if the below type is unnecessary, remove it 
        self.offset = offset
        # @LoveSnowEx FIXME: if the below type is unnecessary, remove it 
        self.tags = tags
        

# !!! Print NBT building size -> (x, y, z)
# def printNbtSize(name: str):
#     nbt_struct = nbt.NBTFile(os.path.join(os.path.join(STRUCTURE_DIR, name), f"{name}.nbt"))
#     x, y, z = getStructureSizeNBT(nbt_struct)
#     print(name, ":", x, y, z)

# !!! Get <building>.json file content in order to parse doorPos, length, width ... information
# def getBuildingInfoDir(name: str):
#     return os.path.join(os.path.join(STRUCTURE_DIR, name), f"{name}.json")

