# for stone, log, food, iron "no amount of human"
# fix: add human transform - SubaRya
from gdpc import WorldSlice
from gdpc.vector_tools import Rect
from ..resource.analyze_material import analyzeSettlementMaterial, analyzeOneBlockVerticalMaterial
from collections import Counter

stoneList = ["minecraft:andesite", "minecraft:basalt", "minecraft:cobblestone", "minecraft:mossy_cobblestone", "minecraft:mossy_stone_bricks", "minecraft:cracked_stone_bricks", "minecraft:diorite",
             "minecraft:dripstone_block", "minecraft:stone", "minecraft:stone_bricks", "minecraft:granite", "minecraft:deepslate", "minecraft:deepslate_bricks", "minecraft:cobbled_deepslate", "minecraft:tuff"]
logList = ["minecraft:oak_log", "minecraft:dark_oak_log", "minecraft:birch_log", "minecraft:spruce_log", "minecraft:jungle_log", "minecraft:acacia_log", "minecraft:stripped_oak_log",
           "minecraft:stripped_birch_log", "minecraft:stripped_spruce_log", "minecraft:stripped_jungle_log", "minecraft:stripped_acacia_log", "minecraft:stripped_dark_oak_log", "minecraft:mangrove_log"]
ironList = ["minecraft:iron_ore", "minecraft:raw_iron_block",
            "minecraft:deepslate_iron_ore"]


class Resource():
    def __init__(self, human: int, wood: int, stone: int, food: int, ironOre: int, iron: int, grass: int):
        self.human = human
        self.wood = wood
        self.stone = stone
        self.food = food
        self.ironOre = ironOre
        self.iron = iron
        self.grass = grass

    def __lt__(self, other):
        return self.grass < other.grass or self.wood < other.wood or self.stone < other.stone or self.food < other.food or self.ironOre < other.ironOre or self.iron < other.iron

    def __sub__(self, other):
        return Resource(
                self.human - other.human, 
                self.wood - other.wood, 
                self.stone - other.stone, 
                self.food - other.food,
                self.ironOre - other.ironOre,
                self.iron - other.iron,
                self.grass - self.grass) 

    def __str__(self):
        return f"human: {self.human}, wood: {self.wood}, stone: {self.stone}, food: {self.food}, ironOre: {self.ironOre}, iron: {self.iron}, grass: {self.grass}"

    def __repr__(self):
        return self.__str__()

class ResourceMap():
    def __init__(self, area: Rect):
        self.human = [[0] * area.size.x] * area.size.y
        self.wood = [[0] * area.size.x] * area.size.y
        self.stone = [[0] * area.size.x] * area.size.y
        self.food = [[0] * area.size.x] * area.size.y
        self.ironOre = [[0] * area.size.x] * area.size.y
        self.iron = [[0] * area.size.x] * area.size.y
        self.grass = [[0] * area.size.x] * area.size.y

    def __str__(self):
        return f"human: {self.human}, wood: {self.wood}, stone: {self.stone}, food: {self.food}, ironOre: {self.ironOre}, iron: {self.iron}, grass: {self.grass}"

    def __repr__(self):
        return self.__str__()



def analyzeResource(materialDict: Counter):
    woodNum = 0
    stoneNum = 0
    foodNum = 0
    ironOreNum = 0
    # ironNum = 0
    for idx in materialDict:
        if idx in logList:
            woodNum += materialDict[idx] * 4
    for idx in materialDict:
        if idx in stoneList:
            stoneNum += materialDict[idx]
    stoneNum //= 10
    for idx in materialDict:
        if idx in ironList:
            ironOreNum += materialDict[idx]
    foodNum += woodNum // 40
    r = Resource(2, woodNum, stoneNum, foodNum, ironOreNum, 0, 10)
    return r

def analyzeAreaMaterialToResource(worldSlice: WorldSlice, area: Rect) -> Resource:
    """
    analyze area material to resource
    """
    materialDict = analyzeSettlementMaterial(worldSlice, area)
    r = analyzeResource(materialDict)
    return r

def getMaterialToResourceMap(worldSlice: WorldSlice, area: Rect) -> ResourceMap:
    rMap = ResourceMap(area)
    for pos in area.inner:
        materialDict = analyzeOneBlockVerticalMaterial(worldSlice, pos)
        r = analyzeResource(Counter(materialDict))
        rMap.human[pos.x][pos.y] = r.human
        rMap.wood[pos.x][pos.y] = r.wood
        rMap.stone[pos.x][pos.y] = r.stone
        rMap.food[pos.x][pos.y] = r.food
        rMap.ironOre[pos.x][pos.y] = r.ironOre
        rMap.iron[pos.x][pos.y] = r.iron
        rMap.grass[pos.x][pos.y] = r.grass
    print(rMap)
    return rMap