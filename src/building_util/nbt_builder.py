from ..resource.biome_substitute import isChangeBlock, changeBlock
import sys
from nbt import nbt as nbt
from typing import Tuple
from gdpc import interface as INTF


def nbtToString(nbt_struct: nbt.TAG):
    match nbt_struct:
        case nbt.TAG_Compound():
            return '{{{}}}'.format(
                ','.join(['{}:{}'.format(str(k), nbtToString(v)) for k, v in nbt_struct.iteritems()]))
        case nbt.TAG_List():
            return '[{}]'.format(','.join([nbtToString(x) for x in nbt_struct]))
        case nbt.TAG_String():
            return '"{}"'.format(str(nbt_struct))
        case nbt.TAG_Byte():
            return '{}b'.format(str(nbt_struct))
        case nbt.TAG_Float():
            return '{}f'.format(str(nbt_struct))
        case nbt.TAG_Double():
            return '{}d'.format(str(nbt_struct))
        case nbt.TAG_Int():
            return '{}'.format(str(nbt_struct))
        case nbt.TAG_Long():
            return '{}'.format(str(nbt_struct))


def buildFromStructureNBT(nbt_struct: nbt.NBTFile, baseX: int, baseY: int, baseZ: int, biome: str, keep=False):
    # fix: isChangeBlock and changeBlock function - SubaRya
    palatte = nbt_struct["palette"]
    for blk in nbt_struct["blocks"]:
        x, y, z = map(lambda e: int(e.value), blk["pos"])
        state = blk["state"].value
        blkName = str(palatte[state]["Name"])
        if "Properties" in palatte[state]:
            blkName += "[{}]".format(','.join(["{}={}".format(str(k), v)
                                               for k, v in palatte[state]["Properties"].iteritems()]))
        if "nbt" in blk:
            blkName += nbtToString(blk["nbt"])
        # INTF.placeBlock(x + baseX, y + baseY, z + baseZ, blkName)
        option = "replace"
        if keep:
            option = "keep"
        # INTF.placeBlock(x + baseX, y + baseY, z + baseZ, blkName)
        if ischangeBlock(biome) == True:
            blkName = changeBlock(biome, blkName)
        # print(blkName)
        INTF.runCommand("/setblock {} {} {} {} {}".format(x +
                        baseX, y + baseY, z + baseZ, blkName, option), 200)


def getStructureSizeNBT(nbt_struct: nbt.NBTFile) -> tuple[int, int, int]:
    size = nbt_struct["size"]
    return (int(str(size[0])), int(str(size[1])), int(str(size[2])))


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        nbt_struct = nbt.NBTFile(fileobj=f)
        buildFromStructureNBT(nbt_struct, 204, 4, 172, "")