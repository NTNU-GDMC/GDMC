import json
import os
from ..resource.terrain_analyzer import Resource
from nbt import nbt

CHALET = "chalet"
DESERT_BUILDING = "desert_building"
HUGE_SAWMILL = "huge_sawmill"


def getJsonAbsPath(name: str, type: int, level: int) -> str:
    # Example: absPath("chalet", 1, 2) -> "...chalet1/level2.json"
    return os.path.abspath(os.path.join(".", os.path.join("data", os.path.join("structures", os.path.join(name + f"{str(type)}", "level" + f"{str(level)}.json")))))


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
    return Resource(human, wood, stone, food, ironOre, iron, grass)


class Entry:
    facing: str
    pos: tuple[int, int, int]

    def __init__(self):
        self.facing = ""
        self.pos = (0, 0, 0)


class BuildingInfo:
    # TODO: BuildingInfo 儲存多個等級的資訊, 提供一支 get 的 api 給 building class 升級時使用
    entriesNameList = []
    entriesInfo = {}
    maxLength: int
    # maxHeight: int
    maxWidth: int
    materialType: str
    buildingType: int
    requiredResource: Resource
    produceResource: Resource

    def __init__(self, filename: str = ""):
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
            r_human = fileData["RequiredResource"]["human"]
            r_wood = fileData["RequiredResource"]["wood"]
            r_stone = fileData["RequiredResource"]["stone"]
            r_food = fileData["RequiredResource"]["food"]
            r_ironOre = fileData["RequiredResource"]["ironOre"]
            r_iron = fileData["RequiredResource"]["iron"]
            r_grass = fileData["RequiredResource"]["grass"]
            self.requiredResource = Resource(
                r_human, r_wood, r_stone, r_food, r_ironOre, r_iron, r_grass)
            p_human = fileData["ProduceResource"]["human"]
            p_wood = fileData["ProduceResource"]["wood"]
            p_stone = fileData["ProduceResource"]["stone"]
            p_food = fileData["ProduceResource"]["food"]
            p_ironOre = fileData["ProduceResource"]["ironOre"]
            p_iron = fileData["ProduceResource"]["iron"]
            p_grass = fileData["ProduceResource"]["grass"]
            self.produceResource = Resource(
                p_human, p_wood, p_stone, p_food, p_ironOre, p_iron, p_grass)

    def getBuildingNameList(self) -> list:
        return self.entriesNameList

    def getEntryInfo(self, name: str) -> Entry:
        return self.entriesInfo[name]

    def getCurrentBuildingLengthAndWidth(self) -> tuple[int, int]:
        return self.maxLength, self.maxWidth

    def getCurrentBuildingType(self):
        return self.buildingType

    def getCurrentBuildingMaterial(self):
        return self.materialType

    def getCurrentRequiredResource(self) -> Resource:
        return self.requiredResource
    
    def getCurrentProduceResource(self) -> Resource:
        return self.produceResource


if __name__ == '__main__':
    target = getJsonAbsPath(CHALET, 1, 2)  # chalet type 1 level 2
    buildingInfo = BuildingInfo(target)
    List = buildingInfo.getBuildingNameList()
    Info = buildingInfo.getEntryInfo("mainEntry")
