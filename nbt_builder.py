import sys
from nbt import nbt as nbt
from gdpc import interface as INTF


def buildFromStructureNBT(nbt_struct: nbt.NBTFile, baseX: int, baseY: int, baseZ: int):
    palatte = nbt_struct["palette"]
    for blk in nbt_struct["blocks"]:
        x, y, z = map(lambda e: int(e.value), blk["pos"])
        state = blk["state"].value
        blkName = str(palatte[state]["Name"])
        if "Properties" in palatte[state]:
            lst = ["{}={}".format(str(k), v)
                   for k, v in palatte[state]["Properties"].iteritems()]
            blkName += "[{}]".format(','.join(lst))
        #INTF.placeBlock(x + baseX, y + baseY, z + baseZ, blkName)
        INTF.runCommand("/setblock {} {} {} {}".format(x +
                        baseX, y + baseY, z + baseZ, blkName))


if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        nbt_struct = nbt.NBTFile(fileobj=f)
        buildFromStructureNBT(nbt_struct, 0, int(input()), 0)
