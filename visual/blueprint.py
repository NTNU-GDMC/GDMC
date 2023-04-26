import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from classes.core import Core

def plotBlueprint(core: Core):
    fig, ax = plt.subplots()

    buildArea = core._editor.getBuildArea()

    for id, building in core._blueprintData.items():
        begin = building.position
        size = building.buildingInfo.getCurrentBuildingLengthAndWidth()
        p = mpatch.Rectangle(begin, size[0], size[1], fill=True, color="blue")
        ax.add_artist(p)
        rx, ry = p.get_xy()
        cx = rx + p.get_width()/2.0
        cy = ry + p.get_height()/2.0
        ax.annotate(f"{id}", (cx, cy), color="w", weight="bold",
                    fontsize=6, ha="center", va="center")

    ax.set_xlim(buildArea.begin.x, buildArea.end.x)
    ax.set_ylim(buildArea.begin.z, buildArea.end.z)
    ax.set_aspect("equal")
    plt.show()
