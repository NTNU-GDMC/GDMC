from random import randint

from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL

dir = {
    "north": (0, 1),
    "east": (1, 0),
    "south": (0, -1),
    "west": (-1, 0),
}


def InitialChalet(x, y, z):
    putChalet(x, y, z)
    putOakDoor(x, y, z, "south")
    putBed(x, y, z, "south")
    putWindow(x, y, z)
    putEastFurnace(x, y, z, "west")
    putWestFurnace(x, y, z, "east")
    putCraftingTable(x, y, z)
    putChest(x, y, z)
    putTorch(x, y, z)


def putChalet(x, y, z):
    for i in range(-1, 2):
        for j in range(-1, 3):
            for k in range(0, 4):
                INTF.placeBlock(x+i, y+j, z+k, "oak_planks")
    INTF.placeBlock(x, y, z+1, "air")
    INTF.placeBlock(x, y+1, z+1, "air")
    INTF.placeBlock(x, y, z+2, "air")
    INTF.placeBlock(x, y+1, z+2, "air")
    # GEO.placeCuboid(x-1,y-1,z,x+1,y+2,z+3,"oak_planks",replace=True,hollow=True)
    INTF.placeBlock(x, y, z, "yellow_bed")


def putOakDoor(x, y, z, facing="north"):
    INTF.placeBlock(x, y, z, f"oak_door[half=lower,facing={facing}]")
    INTF.placeBlock(x, y+1, z, f"oak_door[half=upper,facing={facing}]")


def putBed(x, y, z, facing="north"):
    dx, dz = dir[facing]
    INTF.placeBlock(x+dx, y-1, z+2+dz,
                    f"yellow_bed[part=foot,facing={facing}]")
    INTF.placeBlock(x, y-1, z+2, f"yellow_bed[part=head,facing={facing}]")


def putWindow(x, y, z):
    INTF.placeBlock(x, y+1, z+3, "glass_pane")
    INTF.placeBlock(x, y+2, z+2, "glass")
    INTF.placeBlock(x, y+2, z+1, "glass")
    INTF.placeBlock(x+1, y+1, z+2, "glass_pane")
    INTF.placeBlock(x-1, y+1, z+2, "glass_pane")
    INTF.placeBlock(x+1, y+1, z+1, "glass_pane")
    INTF.placeBlock(x-1, y+1, z+1, "glass_pane")


def putEastFurnace(x, y, z, facing="north"):
    INTF.placeBlock(x+1, y, z+2, f"furnace[facing={facing}]")
    INTF.placeBlock(x+1, y, z+1, f"furnace[facing={facing}]")


def putWestFurnace(x, y, z, facing="north"):
    INTF.placeBlock(x-1, y, z+2, f"furnace[facing={facing}]")
    INTF.placeBlock(x-1, y, z+1, f"furnace[facing={facing}]")


def putCraftingTable(x, y, z):
    INTF.placeBlock(x, y, z+3, "crafting_table")


def putChest(x, y, z, facing="north"):
    INTF.placeBlock(x, y+2, z+3, f"chest[facing={facing}]")


def putTorch(x, y, z, facing="north"):
    INTF.placeBlock(x, y+2, z-1, f"wall_torch[facing={facing}]")
