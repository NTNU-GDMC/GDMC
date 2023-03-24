class Building(object):
    def __init__(self, position: tuple[int, int], length: int, width: int, offset: tuple[int, int] = (0, 0), structureType=None, tags=[]):
        self.position = position
        self.length = length
        self.width = width
        self.offset = offset
        self.structureType = structureType
        self.tags = tags
