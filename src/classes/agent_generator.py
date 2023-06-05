from gdpc.vector_tools import Rect, ivec2
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
    ROCK = auto()


BUILDING_TAGS = {
    CHALET:          [BuildingTag.LAND, BuildingTag.NON_DESERT],
    DESERT_BUILDING: [BuildingTag.LAND, BuildingTag.DESERT],
    SAWMILL:         [BuildingTag.LAND, BuildingTag.NON_DESERT, BuildingTag.FOREST],
    FARM:            [BuildingTag.LAND],
    QUARRY:          [BuildingTag.LAND, BuildingTag.ROCK],
    FORGE:           [BuildingTag.LAND],
    CHURCH:          [BuildingTag.LAND, BuildingTag.CITY]
}


def clampArea(area: Rect, bound: Rect) -> Rect:
    """Clamp the area to the bound"""
    begin, last = area.begin, area.last
    boundBegin, boundLast = bound.begin, bound.last
    begin = ivec2(max(begin.x, boundBegin.x), max(begin.y, boundBegin.y))
    last = ivec2(min(last.x, boundLast.x), min(last.y, boundLast.y))
    return Rect.between(begin, last)


def newBuildAgent(core: Core, name: str):
    tags = BUILDING_TAGS[name]

    def analyzeFunction(core: Core, area: Rect, buildingInfo: BuildingInfo):
        area = area.dilated(config.analyzeBorder)
        buildArea = Rect(size=core.buildArea.toRect().size)

        total = 0

        if nearBound(core, area, config.minimumBoundPadding):
            return 0

        if isVillage(core, area):
            return 0

        if BuildingTag.LAND in tags and isLiquid(core, area):
            return 0

        flatness = isFlat(core, area)
        if flatness < config.flatnessThreshold:
            return 0
        total += flatness

        reqBaseBlock = requiredBasement(core, area)
        # TODO: make this flexible config
        if reqBaseBlock > area.area * 3:
            return 0

        if name in SPECIAL_BUILDINGS:
            if nearBuilding(core, area, buildingInfo, config.minimumBuildingMargin):
                return 0

        if BuildingTag.FOREST in tags:
            queryArea = area.dilated(config.forestQueryMargin)
            clampArea(queryArea, buildArea)
            forestness = hasEnoughWood(core, queryArea)
            if forestness < config.forestThreshold:
                return 0
            total += forestness*10

        if BuildingTag.ROCK in tags:
            queryArea = area.dilated(config.rockQueryMargin)
            queryArea = clampArea(queryArea, buildArea)
            rockness = hasEnoughWood(core, queryArea)
            if rockness < config.rockThreshold:
                return 0
            total += rockness*10

        if BuildingTag.DESERT in tags or BuildingTag.NON_DESERT in tags:
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

    return BuildAgent(core, analyzeFunction, name, cooldown=config.buildAgentCooldown)


def newRoadAgent(core: Core):
    return RoadAgent(core, cooldown=config.roadAgentCooldown)
