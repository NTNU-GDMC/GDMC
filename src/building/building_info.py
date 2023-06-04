import json
from nbt import nbt
from glm import ivec3
from pathlib import Path
from dataclasses import dataclass
from ..config.config import config
from ..resource.terrain_analyzer import Resource

STRUCTURES_PATH = config.structuresPath


@dataclass
class Entry:
    facing: str
    pos: ivec3
    type: str

    @staticmethod
    def fromDict(d: dict) -> "Entry":
        return Entry(d["facing"], ivec3(*d["roadStartPosition"]), d["type"])


@dataclass
class Structure:
    """ Metadata class for each level building info"""
    jsonPath: Path
    nbtPath: Path
    nbtFile: nbt.NBTFile
    level: int
    size: ivec3
    offsets: ivec3
    entries: list[Entry]
    requirement: Resource
    production: Resource

    def __init__(self, jsonPath: Path, nbtPath: Path):
        self.jsonPath = jsonPath
        self.nbtPath = nbtPath
        self.nbtFile = nbt.NBTFile(filename=self.nbtPath)

        with jsonPath.open("r") as f:
            jsonDict = json.load(f)
            self.level = int(jsonDict["Level"])
            self.size = ivec3(*jsonDict["Size"])
            if "Offsets" not in jsonDict:
                self.offsets = ivec3(0, 0, 0)
            else:
                self.offsets = ivec3(jsonDict["Offsets"])
            self.entries = list(map(Entry.fromDict, jsonDict["Entries"]))
            self.requirement = Resource.fromDict(jsonDict["RequiredResource"])
            self.production = Resource.fromDict(jsonDict["ProduceResource"])
            pass


@dataclass
class BuildingInfo:
    """ Metadata class for storing building info """

    # Properties
    name: str
    type: str
    max_size: ivec3
    structures: list[Structure]

    def __init__(self, name: str, variant: dict):
        self.name = name
        self.type = variant["name"]
        # load each level info out of json structure
        self.structures = []
        for level_info in variant["level_info"]:
            jsonPath = STRUCTURES_PATH / level_info["info"]
            nbtPath = STRUCTURES_PATH / level_info["nbt"]
            self.structures.append(Structure(jsonPath, nbtPath))

        # sort level building info by level
        self.structures.sort(key=lambda a: a.level)

        # get max dimensions
        max_length = -1
        max_width = -1
        max_height = -1
        for structure in self.structures:
            max_length = max(max_length, structure.size[0])
            max_height = max(max_height, structure.size[1])
            max_width = max(max_width, structure.size[2])

        self.max_size = ivec3(max_length, max_height, max_width)

    def __str__(self) -> str:
        return f"BuildingInfo(type={self.type})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def maxLevel(self) -> int:
        return len(self.structures)
