import json
import os

class Entry:
    facing :str
    pos: tuple[int, int, int]
    def __init__(self):
        self.facing = ""
        self.pos = (0, 0, 0)

class BuildingInfo:
    entriesNameList = []
    entriesInfo = {}
    def __init__(self, filename: str= ""):
        with open(filename, "r") as f:
            fileData = json.load(f)
            for entry in fileData["Entries"]:
                entryData = Entry()
                entryData.facing = entry["facing"]
                entryData.pos = tuple(entry["roadStartPosition"])
                self.entriesNameList.append(entry["type"])
                self.entriesInfo[entry["type"]] = entryData
    def getBuildingNameList(self) -> list: 
        # for i in self.entriesNameList:
        #     print("Entry Name: ", i)
        return self.entriesNameList
    def getEntryInfo(self, name: str) -> Entry:
        # print("Entry facing:", self.entriesInfo[name].facing)
        # print("Entry position:", self.entriesInfo[name].pos)
        return self.entriesInfo[name]

if __name__ == '__main__':
    target = os.path.abspath("./data/structures/modern_house/modernHouseInfo.json")
    buildingInfo = BuildingInfo(target)
    List = buildingInfo.getBuildingNameList()
    Info = buildingInfo.getEntryInfo("mainEntry")