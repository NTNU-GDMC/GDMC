import json
import os
from BuildingUtil.nbt_builder import getStructureSizeNBT
from resource.ChangeMaterialToResource import resource
from nbt import nbt

CHALET = "chalet"
DESERT_BUILDING = "desert_building"
HUGE_SAWMILL = "huge_sawmill"

# Example: absPath("chalet", 1, 2) -> "...chalet1/level2.json"
def getJsonAbsPath(name: str, type: int, level: int) -> str:
    return os.path.abspath(os.path.join(".",os.path.join("data", os.path.join("structures", os.path.join(name+f"{str(type)}", "level"+f"{str(level)}.json")))))

def getNbtLengthAndWidth(name: str, type: int, level: int) -> tuple[int, int]:
    filename = getJsonAbsPath(name, type, level)
    with open(filename, "r") as f:
        fileData = json.load(f)
        x = fileData["Size"]["length"]
        z = fileData["Size"]["width"]
    return x, z

def getNbtRequiredResource(name: str, type: int, level: int) -> tuple[int, int]:
    filename = getJsonAbsPath(name, type, level)
    with open(filename, "r") as f:
        fileData = json.load(f)
        human = fileData["RequiredResource"]["human"]
        wood = fileData["RequiredResource"]["wood"]
        stone = fileData["RequiredResource"]["stone"]
        food = fileData["RequiredResource"]["food"]
        ironOre = fileData["RequiredResource"]["ironOre"]
        iron = fileData["RequiredResource"]["iron"]
        grass = fileData["RequiredResource"]["grass"]
    return resource(human, wood, stone, food, ironOre, iron, grass)

class Entry:
    facing :str
    pos: tuple[int, int, int]
    def __init__(self):
        self.facing = ""
        self.pos = (0, 0, 0)

# TODO: BuildingInfo 儲存多個等級的資訊, 提供一支 get 的 api 給 building class 升級時使用

class BuildingInfo:
    entriesNameList = []
    entriesInfo = {}
    maxLength: int
    # maxHeight: int
    maxWidth: int
    materialType: str
    buildingType: int
    requiredResource: resource
    def __init__(self, filename: str= ""):
        with open(filename, "r") as f:
            fileData = json.load(f)
            for entry in fileData["Entries"]:
                entryData = Entry()
                entryData.facing = entry["facing"]
                entryData.pos = tuple(entry["roadStartPosition"])
                self.entriesNameList.append(entry["type"])
                self.entriesInfo[entry["type"]] = entryData
            # TODO: get the max Length and Width from level 3 when init class
            self.maxLength = fileData["Size"]["length"]
            # self.maxHeight = fileData["Size"]["height"]
            self.maxWidth = fileData["Size"]["width"]
            # TODO: change material by biome when init class
            self.materialType = fileData["Material"]
            self.buildingType = fileData["Type"]
            # Required material 
            human = fileData["RequiredResource"]["human"]
            wood = fileData["RequiredResource"]["wood"]
            stone = fileData["RequiredResource"]["stone"]
            food = fileData["RequiredResource"]["food"]
            ironOre = fileData["RequiredResource"]["ironOre"]
            iron = fileData["RequiredResource"]["iron"]
            grass = fileData["RequiredResource"]["grass"]
            self.requiredResource = resource(human, wood, stone, food, ironOre, iron, grass)
            
    def getBuildingNameList(self) -> list: 
        # for i in self.entriesNameList:
        #     print("Entry Name: ", i)
        return self.entriesNameList
    def getEntryInfo(self, name: str) -> Entry:
        # print("Entry facing:", self.entriesInfo[name].facing)
        # print("Entry position:", self.entriesInfo[name].pos)
        return self.entriesInfo[name]
    def getCurrentBuildingLengthAndWidth(self) -> tuple[int, int]:
        return self.maxLength, self.maxWidth
    def getCurrentBuildingType(self):
        return self.buildingType
    def getCurrentBuildingMaterial(self):
        return self.materialType
    def getCurrentRequiredResource(self) -> resource:
        return self.requiredResource


if __name__ == '__main__':
    target = getJsonAbsPath(CHALET, 1, 2) # chalet type 1 level 2
    buildingInfo = BuildingInfo(target)
    List = buildingInfo.getBuildingNameList()
    Info = buildingInfo.getEntryInfo("mainEntry")