# for stone, log, food, iron "no amount of human"
# fix: add human transform - SubaRya
from resource.AnalyzeAreaMaterial import analyzeSettlementMaterial

stoneList = ["minecraft:andesite", "minecraft:basalt", "minecraft:cobblestone", "minecraft:mossy_cobblestone", "minecraft:mossy_stone_bricks", "minecraft:cracked_stone_bricks", "minecraft:diorite",
             "minecraft:dripstone_block", "minecraft:stone", "minecraft:stone_bricks", "minecraft:granite", "minecraft:deepslate", "minecraft:deepslate_bricks", "minecraft:cobbled_deepslate", "minecraft:tuff"]
logList = ["minecraft:oak_log", "minecraft:dark_oak_log", "minecraft:birch_log", "minecraft:spruce_log", "minecraft:jungle_log", "minecraft:acacia_log", "minecraft:stripped_oak_log",
           "minecraft:stripped_birch_log", "minecraft:stripped_spruce_log", "minecraft:stripped_jungle_log", "minecraft:stripped_acacia_log", "minecraft:stripped_dark_oak_log", "minecraft:mangrove_log"]
ironList = ["minecraft:iron_ore", "minecraft:raw_iron_block",
            "minecraft:deepslate_iron_ore"]


class resource():
    def __init__(self, human, wood, stone, food, ironOre, iron, grass):
        self.human = human
        self.wood = wood
        self.stone = stone
        self.food = food
        self.ironOre = ironOre
        self.iron = iron
        self.grass = grass

    def printResource(self):
        print(self.human)
        print(self.wood)
        print(self.stone)
        print(self.food)
        print(self.ironOre)
        print(self.iron)
        print(self.grass)


# 需要傳參進來以記錄 resource，如果沒有，我再改成 return 這些值回去
def changeMaterialToResource(worldslice, buildArea) -> resource:
    material, materialList = analyzeSettlementMaterial(worldslice, buildArea)
    # print(materialList)
    # print("----------------")
    # print(material)
    woodNum = 0
    stoneNum = 0
    foodNum = 0
    ironOreNum = 0
    # ironNum = 0
    for idx in materialList:
        if idx in logList:
            woodNum += materialList[idx]*4
    for idx in materialList:
        if idx in stoneList:
            stoneNum += materialList[idx]
    stoneNum //= 10
    for idx in materialList:
        if idx in ironList:
            ironOreNum += materialList[idx]
    foodNum += woodNum // 40
    #  TODO: human will be count on settlement size - SubaRya
    r = resource(2, woodNum, stoneNum, foodNum, ironOreNum, 0, 10)
    # r.printResource()
    return r
    # print("woodNum: ", woodNum)
    # print("stoneNum: ", stoneNum)
    # print("foodNum: ", foodNum)
    # print("ironOreNum: ", ironOreNum)
