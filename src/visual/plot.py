import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def plotContour(heights: np.ndarray, spacing=8):
    Y = np.transpose(heights)
    levels = np.arange(0, 256, spacing)
    im = plt.imshow(Y, cmap=cm.Greys)
    cset = plt.contour(Y, levels=levels, linewidths=1, cmap=cm.Dark2)
    plt.colorbar(im)
    plt.clabel(cset, inline=True, fmt='%d', fontsize=10)
    plt.show()


if __name__ == "__main__":
    # Test
    from classes.core import Core
    core = Core()
    worldSlice = core._editor.worldSlice
    heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    plotContour(heights)
