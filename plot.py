import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# ---------------------------------------- #

from gdpc import interface as INTF
from gdpc import worldLoader as WL
from interface import Interface

intf = Interface()

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = buildArea = (0, 1, 0, 255, 255, 255)

intf.runCommand(
    f"/setbuildarea {STARTX} {STARTY} {STARTZ} {ENDX} {ENDY} {ENDZ}", 0)
print("Build Area: ", *INTF.requestBuildArea())

WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
heights: np.ndarray = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

# ---------------------------------------- #
step = 1

x = np.arange(STARTX, ENDX+1, step, dtype=int)
z = np.arange(STARTZ, ENDZ+1, step, dtype=int)

Z, X = np.meshgrid(z, x)
Y = np.array([[int(heights[(_x, _z)]) for _z in z] for _x in x])

print("X:", X)
print("Z:", Z)
print("Y:", Y)

# exit(0)

ax = plt.axes(projection='3d')
ax.plot_wireframe(Z, X, Y)
ax.plot_surface(Z, X, Y, cmap=cm.coolwarm)
ax.set_xlabel('z')
ax.set_ylabel('x')
ax.set_zlabel('y')
ax.set_box_aspect((1, 1, 0.1))
plt.title('Axes3D Plot Surface')
plt.show()
