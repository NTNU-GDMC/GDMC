from math import ceil
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from ..classes.core import Core
from ..config.config import config

UNIT = config.unit

def fitToGrid(x: int) -> float:
    return ceil(x/UNIT)*UNIT

def plotBlueprint(core: Core):
    fig, ax = plt.subplots()

    buildArea = core._editor.getBuildArea()
    offset = buildArea.toRect().offset

    for id, building in core.blueprintData.items():
        begin = building.position + offset
        size = building.currentSize
        maxSize = building.maxSize
        p = mpatch.Rectangle(begin, fitToGrid(maxSize.x), fitToGrid(maxSize.z), fill=True, color="gray")
        ax.add_artist(p)
        p = mpatch.Rectangle(begin, fitToGrid(size.x), fitToGrid(size.z), fill=True, color="blue")
        ax.add_artist(p)
        rx, ry = p.get_xy()
        cx = rx + p.get_width() / 2.0
        cy = ry + p.get_height() / 2.0
        ax.annotate(f"{id}", (cx, cy), color="w", weight="bold",
                    fontsize=6, ha="center", va="center")

    for node in core.roadNetwork.subnodes:
        p = mpatch.Rectangle(node.val + offset, UNIT, UNIT, fill=True, color="red")
        ax.add_artist(p)

    ax.set_xlim(buildArea.begin.x, buildArea.end.x)
    ax.set_ylim(buildArea.begin.z, buildArea.end.z)
    ax.set_aspect("equal")
    plt.show()
