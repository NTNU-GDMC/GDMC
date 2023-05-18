import json
from dataclasses import dataclass
from pathlib import Path
from gdpc.vector_tools import Box

DEFAULT_CONFIG_PATH = Path("config.json")


@dataclass
class Config:
    """Config class for storing config data"""

    # buildArea is the area where buildings can be built
    buildArea: Box = Box((0, 0, 0), (255, 255, 255))

    # unit is the size of a single unit on the map
    unit: int = 2

    def save(self, path: Path = DEFAULT_CONFIG_PATH):
        """Save config to a json file"""
        with open(path, "w") as f:
            json.dump(self.__dict__, f, indent=4)

    @staticmethod
    def load(path: Path = DEFAULT_CONFIG_PATH):
        """Load config from a json file"""
        if not path.exists():
            return Config()
        with open(path, "r") as f:
            data = json.load(f)
        return Config(**data)


config = Config.load()
