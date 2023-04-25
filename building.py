class Building(object):
    def __init__(self, nbtName:str, level: int, position: tuple[int, int], doorPos: tuple[int, int], length: int, width: int, offset: tuple[int, int] = (0, 0), materialType=None, tags=[]):
        self.nbtName = nbtName              # building name
        self.level = level                  # building level: 1~3
        self.position = position            # building coord
        self.doorPos = doorPos              # door coord
        self.length = length                # max length in this type of building
        self.width = width                  # max width in this type of building
        self.materialType = materialType    # building material
        self.offset = offset                # ???
        self.tags = tags                    # ???
