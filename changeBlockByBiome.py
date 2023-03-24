# fix: all list need to be fixed - SubaRya
import re

originTosnowList = {
    "oak_planks": "spruce_planks",
    "oak_door": "spruce_door",
    "oak_log": "spruce_log",
    "oak_wood": "spruce_wood",
    "oak_slab": "spruce_slab",
    "oak_door": "spruce_door",
    "oak_sign": "spruce_sign",
    "oak_fence": "spruce_fence",
    "oak_planks": "spruce_planks",
    "oak_leaves": "spruce_leaves",
    "oak_stairs": "spruce_stairs",
    "oak_button": "spruce_button",
    "oak_sapling": "spruce_sapling",
    "oak_trapdoor": "spruce_trapdoor",
    "oak_wall_sign": "spruce_wall_sign",
    "oak_fence_gate": "spruce_fence_gate",
    "oak_pressure_plate": "spruce_pressure_plate",
    "stripped_oak_log": "stripped_spruce_log",
    "stripped_oak_wood": "stripped_spruce_wood",
    "potted_oak_sapling": "minecraft:potted_spruce_sapling",
}


def snowRepl(m):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originTosnowList[parseX])
    return ":" + parseX


def ischangeBlock(biome: str):
    if biome == "snow" or biome == "badland":
        return True
    return False

# This function will change block definitely via biome


def changeBlock(biome: str, blockName: str):
    if biome == "snow":
        blockName = re.sub(r":[\w_]*\b", snowRepl, blockName)
    return blockName
