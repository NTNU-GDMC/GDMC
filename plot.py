import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def plotContour(heights, spacing=8):
    Y = heights.T[:-1, :-1]
    levels=np.arange(0, 256, spacing)
    im = plt.imshow(Y, cmap=cm.Greys)
    cset = plt.contour(Y, levels=levels, linewidths=1, cmap=cm.Dark2)
    plt.colorbar(im)
    plt.clabel(cset, inline=True, fmt='%d', fontsize=10)
    plt.show()
