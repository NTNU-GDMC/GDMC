# fix: all list need to be fixed - SubaRya
import re

originToSpruceList = {
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

originToBirchList = {
    "oak_planks": "birch_planks",
    "oak_door": "birch_door",
    "oak_log": "birch_log",
    "oak_wood": "birch_wood",
    "oak_slab": "birch_slab",
    "oak_door": "birch_door",
    "oak_sign": "birch_sign",
    "oak_fence": "birch_fence",
    "oak_planks": "birch_planks",
    "oak_leaves": "birch_leaves",
    "oak_stairs": "birch_stairs",
    "oak_button": "birch_button",
    "oak_sapling": "birch_sapling",
    "oak_trapdoor": "birch_trapdoor",
    "oak_wall_sign": "birch_wall_sign",
    "oak_fence_gate": "birch_fence_gate",
    "oak_pressure_plate": "birch_pressure_plate",
    "stripped_oak_log": "stripped_birch_log",
    "stripped_oak_wood": "stripped_birch_wood",
    "potted_oak_sapling": "minecraft:potted_birch_sapling",
}

originToJungleList = {
    "oak_planks": "jungle_planks",
    "oak_door": "jungle_door",
    "oak_log": "jungle_log",
    "oak_wood": "jungle_wood",
    "oak_slab": "jungle_slab",
    "oak_door": "jungle_door",
    "oak_sign": "jungle_sign",
    "oak_fence": "jungle_fence",
    "oak_planks": "jungle_planks",
    "oak_leaves": "jungle_leaves",
    "oak_stairs": "jungle_stairs",
    "oak_button": "jungle_button",
    "oak_sapling": "jungle_sapling",
    "oak_trapdoor": "jungle_trapdoor",
    "oak_wall_sign": "jungle_wall_sign",
    "oak_fence_gate": "jungle_fence_gate",
    "oak_pressure_plate": "jungle_pressure_plate",
    "stripped_oak_log": "stripped_jungle_log",
    "stripped_oak_wood": "stripped_jungle_wood",
    "potted_oak_sapling": "minecraft:potted_jungle_sapling",
}

originToAcaciaList = {
    "oak_planks": "acacia_planks",
    "oak_door": "acacia_door",
    "oak_log": "acacia_log",
    "oak_wood": "acacia_wood",
    "oak_slab": "acacia_slab",
    "oak_door": "acacia_door",
    "oak_sign": "acacia_sign",
    "oak_fence": "acacia_fence",
    "oak_planks": "acacia_planks",
    "oak_leaves": "acacia_leaves",
    "oak_stairs": "acacia_stairs",
    "oak_button": "acacia_button",
    "oak_sapling": "acacia_sapling",
    "oak_trapdoor": "acacia_trapdoor",
    "oak_wall_sign": "acacia_wall_sign",
    "oak_fence_gate": "acacia_fence_gate",
    "oak_pressure_plate": "acacia_pressure_plate",
    "stripped_oak_log": "stripped_acacia_log",
    "stripped_oak_wood": "stripped_acacia_wood",
    "potted_oak_sapling": "minecraft:potted_acacia_sapling",
}

originToDarkOakList = {
    "oak_planks": "dark_oak_planks",
    "oak_door": "dark_oak_door",
    "oak_log": "dark_oak_log",
    "oak_wood": "dark_oak_wood",
    "oak_slab": "dark_oak_slab",
    "oak_door": "dark_oak_door",
    "oak_sign": "dark_oak_sign",
    "oak_fence": "dark_oak_fence",
    "oak_planks": "dark_oak_planks",
    "oak_leaves": "dark_oak_leaves",
    "oak_stairs": "dark_oak_stairs",
    "oak_button": "dark_oak_button",
    "oak_sapling": "dark_oak_sapling",
    "oak_trapdoor": "dark_oak_trapdoor",
    "oak_wall_sign": "dark_oak_wall_sign",
    "oak_fence_gate": "dark_oak_fence_gate",
    "oak_pressure_plate": "dark_oak_pressure_plate",
    "stripped_oak_log": "stripped_dark_oak_log",
    "stripped_oak_wood": "stripped_dark_oak_wood",
    "potted_oak_sapling": "minecraft:potted_dark_oak_sapling",
}


def spruceRepl(m):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToSpruceList[parseX])
    return ":" + parseX

def birchRepl(m):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToBirchList[parseX])
    return ":" + parseX

def jungleRepl(m):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToJungleList[parseX])
    return ":" + parseX

def acaciaRepl(m):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToAcaciaList[parseX])
    return ":" + parseX

def darkOakRepl(m):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToDarkOakList[parseX])
    return ":" + parseX

"""
material: biome => 
    spruce: taiga, snowy_tundra, snowy_mountains, taiga_hills, snowy_beach, 
            snowy_taiga, snowy_taiga_hills, giant_tree_taiga,
            giant_tree_taiga_hills, taiga_mountains, ice_spikes,
            snowy_taiga_mountains, giant_spruce_taiga, giant_spruce_taiga_hills
    birch: forest, birch_forest, birch_forest_hills, flower_forest, tall_birch_forest, tall_birch_hills
    jungle:jungle, jungle_hills, jungle_edge, modified_jungle, modified_jungle_edge
    acacia: savanna, savanna_plateau, shattered_savanna, shattered_savanna_plateau
    dark_oak: dark_forest, dark_forest_hills
    desert: desert, desert_hills, desert_lakes
    oak: other
"""

spruceSet = {
    "taiga", "snowy_tundra", "snowy_mountains", "taiga_hills", "snowy_beach",
    "snowy_taiga", "snowy_taiga_hills", "giant_tree_taiga",
    "giant_tree_taiga_hills", "taiga_mountains", "ice_spikes",
    "snowy_taiga_mountains", "giant_spruce_taiga", "giant_spruce_taiga_hills"
}
birchSet = {
    "forest", "birch_forest", "birch_forest_hills", "flower_forest", "tall_birch_forest", "tall_birch_hills"
}
jungleSet = {
    "jungle", "jungle_hills", "jungle_edge", "modified_jungle", "modified_jungle_edge"
}
acaciaSet = {
    "savanna", "savanna_plateau", "shattered_savanna", "shattered_savanna_plateau"
}
darkOakSet = {
    "dark_forest", "dark_forest_hills"
}
desertSet = {
    "desert", "desert_hills", "desert_lakes"
}

def getChangeMaterialList(biomeList: list[str]) -> list[str]:
    retList: list[str] = []
    for biome in biomeList:
        if biome in spruceSet:
            if("spruce" not in retList):
                retList.append("spruce")
        elif biome in birchSet:
            if("birch" not in retList):
                retList.append("birch")
        elif biome in jungleSet:
            if("jungle" not in retList):
                retList.append("jungle")
        elif biome in acaciaSet:
            if("acacia" not in retList):
                retList.append("acacia")
        elif biome in darkOakSet:
            if("dark_oak" not in retList):
                retList.append("dark_oak")
        elif biome in desertSet:
            return ["desert"]
    if(("spruce" not in retList) and ("dark_oak" not in retList)):
        retList.append("oak")
    return retList

def changeBlock(material: str, blockName: str):
    # This function will change block definitely via building_info material
    if material == "spruce":
        blockName = re.sub(r":[\w_]*\b", spruceRepl, blockName)
    elif material == "birch":
        blockName = re.sub(r":[\w_]*\b", birchRepl, blockName)
    elif material == "jungle":
        blockName = re.sub(r":[\w_]*\b", jungleRepl, blockName)
    elif material == "acacia":
        blockName = re.sub(r":[\w_]*\b", acaciaRepl, blockName)
    elif material == "dark_oak":
        blockName = re.sub(r":[\w_]*\b", darkOakRepl, blockName)
    return blockName
