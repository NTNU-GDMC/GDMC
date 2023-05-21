"""
1. absPath = getNBTAbsPath(name, type, level)
    - get the absolute path of the nbt file.
        - name, level can be found in src/building_util/building.py
        - type can be found in src/building_util/building_info.py
2. nbt_struct = nbt.NBTFile(absPath)
    - get the nbt structure.
3. buildFromStructureNBT(nbt_struct, baseX, baseY, baseZ, biome)
    - build the structure
    - biome default is "".
"""

from ..resource.biome_substitute import isChangeBlock, changeBlock
import os
from nbt import nbt as nbt
from gdpc import Editor, Block, Box
from gdpc.vector_tools import ivec3
from src.building.building_info import CHALET, DESERT_BUILDING


def getNBTAbsPath(name: str, type: int, level: int) -> str:
    # Example: getNBTAbsPath("chalet", 1, 2) -> "...chalet1/level2.nbt"
    return os.path.abspath(os.path.join(".", os.path.join("data", os.path.join("structures", os.path.join(name + f"{str(type)}", "level" + f"{str(level)}.nbt")))))


def NBT2Str(struct: nbt.TAG):
    match struct:
        case nbt.TAG_Compound():
            return '{{{}}}'.format(
                ','.join(['{}:{}'.format(str(k), NBT2Str(v)) for k, v in struct.iteritems()]))
        case nbt.TAG_List():
            return '[{}]'.format(','.join([NBT2Str(x) for x in struct]))
        case nbt.TAG_String():
            return '"{}"'.format(str(struct))
        case nbt.TAG_Byte():
            return '{}b'.format(str(struct))
        case nbt.TAG_Float():
            return '{}f'.format(str(struct))
        case nbt.TAG_Double():
            return '{}d'.format(str(struct))
        case nbt.TAG_Int():
            return '{}'.format(str(struct))
        case nbt.TAG_Long():
            return '{}'.format(str(struct))


def NBT2Blocks(struct: nbt.NBTFile, offset: ivec3 = ivec3(0, 0, 0)):
    palatte = struct["palette"]
    for blk in struct["blocks"]:
        pos = ivec3(*map(lambda p: int(p.value), blk["pos"]))
        stateTag = palatte[blk["state"].value]
        block = Block.fromBlockStateTag(stateTag)
        yield pos + offset, block


def buildFromNBT(editor: Editor, struct: nbt.NBTFile, offset: ivec3, biome: str = "", keep=False):
    if editor.worldSlice is None:
        raise Exception("Error while building structure: worldSlice is None")

    option = "keep" if keep else "replace"

    if not keep:
        size = getStructureSizeNBT(struct)
        bound = Box(offset, size)
        begin = bound.begin
        last = bound.last
        clearCmd = f"fill {begin.x} {begin.y} {begin.z} {last.x} {last.y} {last.z} barrier"
        editor.runCommand(clearCmd, syncWithBuffer=True)

    for pos, block in NBT2Blocks(struct, offset):
        # FIXME: isChangeBlock and changeBlock function - SubaRya
        # if isChangeBlock(biome) == True:
        #     blkName = changeBlock(biome, blkName)

        cmd = f"setblock {pos.x} {pos.y} {pos.z} {block} {option}"

        editor.runCommand(cmd, syncWithBuffer=True)


def getStructureSizeNBT(struct: nbt.NBTFile) -> ivec3:
    size = struct["size"]
    return ivec3(*map(lambda x: int(x.value), size))


def getBuildingNBTDir(name: str, type: int, level: int):
    return getNBTAbsPath(name, type, level)
