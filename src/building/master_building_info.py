import json
from dataclasses import dataclass
from src.building.building_info import BuildingInfo, STRUCTURES_PATH

@dataclass
class MasterBuildingInfo:
    """
    Building root data class
    Buildings are crammed in one dictionary and different variants are spread in the corresponding list.
    """

    buildings: dict[str, list[BuildingInfo]]

    def __init__(self):
        self.buildings = {}
        with (STRUCTURES_PATH/"buildings.json").open("r") as f:
            parsed_data: dict = json.load(f)
            for k, building_parent_obj in parsed_data.items():
                self.buildings[k] = []
                for val in building_parent_obj["variants"]:
                    self.buildings[k].append(BuildingInfo(k, val))

    def __getitem__(self, key: str) -> list[BuildingInfo]:
        """ Get building info by its key """
        return self.buildings[key]


""" Singleton pattern root data instance """
GLOBAL_BUILDING_INFO = MasterBuildingInfo()
