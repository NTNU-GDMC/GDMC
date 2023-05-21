import json
import os

from glm import ivec3
from pathlib import Path

from ..resource.terrain_analyzer import Resource

CHALET = "chalet"
DESERT_BUILDING = "desert_building"
HUGE_SAWMILL = "huge_sawmill"
STRUCTURES_PATH = Path("data/structures")


def getJsonAbsPath(name: str, type: int, level: int) -> Path:
    # Example: absPath("chalet", 1, 2) -> "...chalet1/level2.json"
    return STRUCTURES_PATH/f"{name}{type}/level{level}.json"


def getNbtLengthAndWidth(name: str, type: int, level: int) -> tuple[int, int]:
    filename = getJsonAbsPath(name, type, level)
    with open(filename, "r") as f:
        fileData = json.load(f)
        x = fileData["Size"]["length"]
        z = fileData["Size"]["width"]
    return x, z


def getNbtRequiredResource(name: str, type: int, level: int) -> Resource:
    filename = getJsonAbsPath(name, type, level)
    with open(filename, "r") as f:
        file_data = json.load(f)
        human = file_data["RequiredResource"]["human"]
        wood = file_data["RequiredResource"]["wood"]
        stone = file_data["RequiredResource"]["stone"]
        food = file_data["RequiredResource"]["food"]
        iron_ore = file_data["RequiredResource"]["ironOre"]
        iron = file_data["RequiredResource"]["iron"]
        grass = file_data["RequiredResource"]["grass"]
    return Resource(human, wood, stone, food, iron_ore, iron, grass)


class Entry:
    facing: str
    pos: tuple[int, int, int]
    type: str

    def __init__(self, facing, pos, type_):
        self.facing = facing
        self.pos = pos
        self.type = type_


class LevelBuildingInfo:
    """ Metadata class for each level building info"""
    size: ivec3
    entries: list[Entry]
    material: str
    level: int
    resource: Resource
    nbt_path: str

    def init(self, size: ivec3, entries: list[Entry], material: str, level: int,
             resource: Resource):
        # x, z dimension need to be confirmed, this is a PoC
        self.size = size
        self.entries = entries
        self.level = level
        self.material = material
        self.resource = resource

    def __init__(self, json_path: str, nbt_path: str):
        self.nbt_path = nbt_path

        with open(json_path, "r") as f:
            json_dict = json.load(f)

            entries = []
            for entry in json_dict["Entries"]:
                entries.append(Entry(entry["facing"], tuple(
                    entry["roadStartPosition"]), entry["type"]))

            w, h, l = json_dict["Size"]["width"], json_dict["Size"]["height"], json_dict["Size"]["length"]
            size = ivec3(w, h, l)

            # TODO: change material by biome when init

            # call real init
            self.init(size, entries, json_dict["Material"], int(json_dict["Level"]),
                      Resource.fromDict(json_dict["RequiredResource"]))


class BuildingInfo:
    """ Metadata class for storing building info """

    # Properties
    max_length: int
    max_height: int
    max_width: int
    level_building_info: list[LevelBuildingInfo]
    type: str

    def __init__(self, variant):
        self.type = variant["name"]
        # load each level info out of json structure
        self.level_building_info = []
        for var in variant["level_info"]:
            self.level_building_info.append(LevelBuildingInfo(os.path.join(STRUCTURES_PATH, var["info"]),
                                                                   os.path.join(STRUCTURES_PATH, var["nbt"])))

        # sort level building info by level
        self.level_building_info.sort(key=lambda a: a.level)

        # get max dimensions
        self.max_length = -1
        self.max_width = -1
        self.max_height = -1
        for lbi in self.level_building_info:
            self.max_length = max(self.max_length, lbi.size[0])
            self.max_width = max(self.max_width, lbi.size[2])
            self.max_height = max(self.max_height, lbi.size[1])

    # TODO: 提供一支 get 的 api 給 building class 升級時使用

    @property
    def dimension(self):
        return ivec3([self.max_width, self.max_height, self.max_length])
