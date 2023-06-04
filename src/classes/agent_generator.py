from typing import Callable
from gdpc.vector_tools import Rect
from enum import Enum, auto
from ..classes.core import Core
from ..classes.agent import BuildAgent, RoadAgent
from ..analyze_util.basic import isFlat, hasEnoughWood, closeEnoughToRoad, isLiquid, isDesert, nearBound, requiredBasement, nearBuilding, isVillage
from ..config.config import config
from ..building.building_info import BuildingInfo


# basic buildings

CHALET = "chalet"
DESERT_BUILDING = "desert_building"

BASIC_BUILDINGS = {
    CHALET,
    DESERT_BUILDING
}

# Special buildings

SAWMILL = "sawmill"
FARM = "farm"
QUARRY = "quarry"
FORGE = "forge"
CHURCH = "church"

SPECIAL_BUILDINGS = {
    SAWMILL,
    FARM,
    QUARRY,
    FORGE,
    CHURCH
}

# Building tags


class BuildingTag(Enum):
    LAND = auto()
    DESERT = auto()
    NON_DESERT = auto()
    CITY = auto()
    FOREST = auto()


BUILDING_TAGS = {
    CHALET:          [BuildingTag.LAND, BuildingTag.NON_DESERT],
    DESERT_BUILDING: [BuildingTag.LAND, BuildingTag.DESERT],
    SAWMILL:         [BuildingTag.LAND, BuildingTag.NON_DESERT, BuildingTag.FOREST],
    FARM:            [BuildingTag.LAND],
    QUARRY:          [BuildingTag.LAND],
    FORGE:           [BuildingTag.LAND],
    CHURCH:          [BuildingTag.LAND, BuildingTag.CITY]
}


def newBuildAgent(core: Core, name: str):
    tags = BUILDING_TAGS[name]

    def analyzeFunction(core: Core, area: Rect, buildingInfo: BuildingInfo):
        area = area.dilated(config.analyzeBorder)

        total = 0

        if nearBound(core, area):
            return 0

        if isVillage(core, area):
            return 0

        reqBaseBlock = requiredBasement(core, area)
        # TODO: make this flexible config
        if reqBaseBlock > area.area * 3:
            return 0

        flatness = isFlat(core, area)
        if flatness < config.flatnessThreshold:
            return 0
        total += flatness

        if name in SPECIAL_BUILDINGS:
            if nearBuilding(core, area, buildingInfo, config.minimumBuildingMargin):
                return 0

        if BuildingTag.LAND in tags and isLiquid(core, area):
            return 0

        if BuildingTag.FOREST in tags:
            buildArea = Rect((0, 0), core.buildArea.toRect().size)
            queryArea = area.dilated(config.forestQueryMargin)
            begin, end = queryArea.begin, queryArea.end
            begin.x = max(begin.x, buildArea.begin.x)
            begin.y = max(begin.y, buildArea.begin.y)
            end.x = min(end.x, buildArea.end.x)
            end.y = min(end.y, buildArea.end.y)
            queryArea = Rect(begin, end-begin)
            forestness = hasEnoughWood(core, queryArea)
            if forestness < config.forestThreshold:
                return 0
            total += forestness*10

        desertness = isDesert(core, area)
        if BuildingTag.DESERT in tags:
            if desertness <= config.desertnessThreshold:
                return 0
            total += desertness
        if BuildingTag.NON_DESERT in tags:
            if desertness >= config.desertnessThreshold:
                return 0
            total += 1-desertness

        return total

    return BuildAgent(core, analyzeFunction, name)


def newRoadAgent(core: Core):
    return RoadAgent(core)
