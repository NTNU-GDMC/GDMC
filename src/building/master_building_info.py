import json
import os

from src.building.building_info import BuildingInfo, STRUCTURES_PATH


class MasterBuildingInfo:
    """
    Building root data class
    Buildings are crammed in one dictionary and different variants are spread in the corresponding list.
    """

    buildings: dict[str, list[BuildingInfo]]

    def __init__(self):
        self.buildings = {}
        with open(os.path.join(STRUCTURES_PATH, "buildings.json"), "r") as f:
            parsed_data = json.load(f)
            for k, building_parent_obj in parsed_data.items():
                self.buildings[k] = []
                for val in building_parent_obj["variants"]:
                    self.buildings[k].append(BuildingInfo(val))

    def get_buildings_by_key(self, key: str) -> list[BuildingInfo]:
        """ Get building info by its key """
        return self.buildings[key]


""" Singleton pattern root data instance """
GLOBAL_BUILDING_INFO = MasterBuildingInfo()
