# fix: all list need to be fixed - SubaRya
from re import compile, Match

"""
Material Replace Table based on nbt building default material
"""

originToSpruceDict = {
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
    "potted_oak_sapling": "potted_spruce_sapling",
}

originToBirchDict = {
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
    "potted_oak_sapling": "potted_birch_sapling",
}

originToJungleDict = {
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
    "potted_oak_sapling": "potted_jungle_sapling",
}

originToAcaciaDict = {
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
    "potted_oak_sapling": "potted_acacia_sapling",
}

originToDarkOakDict = {
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
    "potted_oak_sapling": "potted_dark_oak_sapling",
}

originToRedSandDict = {
    "sand": "red_sand",
    "sandstone": "red_sandstone",
    "sandstone_slab": "red_sandstone_slab",
    "sandstone_wall": "red_sandstone_wall",
    "sandstone_stairs": "red_sandstone_stairs",
    "smooth_sandstone_slab": "smooth_red_sandstone_slab",
    "smooth_sandstone_stairs": "smooth_red_sandstone_stairs",
    "smooth_sandstone": "smooth_red_sandstone",
    "cut_sandstone_slab": "cut_red_sandstone_slab",
    "cut_sandstone": "cut_red_sandstone",
    "chiseled_sandstone": "chiseled_red_sandstone",
}


"""
Material Replace function
"""


def spruceRepl(m: Match[str]):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToSpruceDict[parseX])
    return ":" + parseX


def birchRepl(m: Match[str]):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToBirchDict[parseX])
    return ":" + parseX


def jungleRepl(m: Match[str]):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToJungleDict[parseX])
    return ":" + parseX


def acaciaRepl(m: Match[str]):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToAcaciaDict[parseX])
    return ":" + parseX


def darkOakRepl(m: Match[str]):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("oak") or parseX.startswith("stripped_oak") or parseX.startswith("potted_oak"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToDarkOakDict[parseX])
    return ":" + parseX


def redSandRepl(m: Match[str]):
    x = m.group()
    parseX = str(x[1:])
    if parseX.startswith("sand") or parseX.startswith("sandstone") or parseX.startswith("smooth_sandstone") or parseX.startswith("cut_sandstone") or parseX.startswith("chiseled_sandstone"):
        # print("x= ", parseX)
        parseX = parseX.replace(parseX, originToRedSandDict[parseX])
    return ":" + parseX


"""
Material <=>  Biome
According to Java edition.
"""

spruceSet = {
    "minecraft:snowy_plains", "minecraft:ice_spikes", "minecraft:old_growth_pine_taiga", "minecraft:old_growth_spruce_taiga",
    "minecraft:taiga", "minecraft:snowy_taiga", "minecraft:windswept_hills", "minecraft:windswept_forest",
    "minecraft:grove", "minecraft:snowy_slopes", "minecraft:frozen_peaks", "minecraft:jagged_peaks", "minecraft:snowy_beach"
}

birchSet = {
    "minecraft:birch_forest", "minecraft:old_growth_birch_forest", "minecraft:meadow"
}

jungleSet = {
    "minecraft:jungle", "minecraft:sparse_jungle", "minecraft:bamboo_jungle"
}

acaciaSet = {
    "minecraft:savanna", "minecraft:savanna_plateau", "minecraft:windswept_savanna"
}

darkOakSet = {
    "minecraft:dark_forest"
}

otherSet = {
    "minecraft:flower_forest", "minecraft:windswept_hills", "minecraft:windswept_forest", "minecraft:bamboo_jungle",
    "minecraft:wooded_badlands"
}

desertSet = {
    "minecraft:desert", "minecraft:beach"
}

redSandSet = {
    "minecraft:badlands", "minecraft:eroded_badlands", "minecraft:wooded_badlands"
}


def getChangeMaterial(biome: str) -> str:
    """return change material according to biome"""

    if biome in spruceSet:
        return "spruce"
    if biome in birchSet:
        return "birch"
    if biome in jungleSet:
        return "jungle"
    if biome in acaciaSet:
        return "acacia"
    if biome in darkOakSet:
        return "dark_oak"
    if biome in desertSet:
        return "sand"
    if biome in redSandSet:
        return "red_sand"
    if biome in otherSet:
        return "oak"

    return "oak"


def getChangeMaterialList(biomeList: list[str]) -> list[str]:
    """
        This function return maybe list for
        1. pure wood
        2. pure sand
        3. wood and sand
    """
    materials = set[str]()
    for biome in biomeList:
        material = getChangeMaterial(biome)
        materials.add(material)
    """and ("sand" not in retList) and ("red_sand" not in retList)"""
    if (("spruce" not in materials) and ("dark_oak" not in materials)):
        materials.add("oak")
    return list(materials)


def changeBlock(material: str, blockName: str):
    # This function will change block definitely via building_info material
    pattern = compile(r":[\w_]*\b")
    if material == "spruce":
        blockName = pattern.sub(spruceRepl, blockName)
    elif material == "birch":
        blockName = pattern.sub(birchRepl, blockName)
    elif material == "jungle":
        blockName = pattern.sub(jungleRepl, blockName)
    elif material == "acacia":
        blockName = pattern.sub(acaciaRepl, blockName)
    elif material == "dark_oak":
        blockName = pattern.sub(darkOakRepl, blockName)
    elif material == "red_sand":
        blockName = pattern.sub(redSandRepl, blockName)
    return blockName
