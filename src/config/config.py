"""
This module contains the Config class for storing config data.
You can save and load config data to and from a json file.
Add new config data to the Config class and it will be able to save and load.

Example:
    Get the config data:
        >>> from src.config.config import config
        >>> buildArea = config.buildArea
        >>> unit = config.unit

    Modify the config class:
        class Config:
            buildArea: Box = Box((0, 0, 0), (255, 255, 255))
            unit: int = 2

            # You can add new config data here:
            dataStructuresPath: Path = Path("data/structures")

    Save the config data:
        >>> config.save("custom_config.json")

    Load the custom config data:
        >>> config = Config.load("custom_config.json")
"""

import json
from dataclasses import dataclass
from pathlib import Path
from gdpc.vector_tools import Box
from .generic_json import GenericJSONEncoder, GenericJSONDecoder

DEFAULT_CONFIG_PATH = Path("config.json")


@dataclass
class Config:
    """Config class for storing config data"""

    # buildArea is the area where buildings can be built
    buildArea: Box = Box((0, 0, 0), (255, 255, 255))

    # unit is the size of a single unit on the map
    unit: int = 2

    #* You can add new config data here:

    def save(self, path: Path = DEFAULT_CONFIG_PATH):
        """Save config to a json file"""
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with path.open("w") as f:
            json.dump(self, f, indent=4, cls=GenericJSONEncoder)

    @staticmethod
    def load(path: Path = DEFAULT_CONFIG_PATH) -> "Config":
        """Load config from a json file"""
        if not path.exists():
            return Config()
        with path.open("r") as f:
            data: Config = json.load(f, cls=GenericJSONDecoder)
            return data


config = Config.load()
