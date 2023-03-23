from gdpc import Editor
from gdpc.vector_tools import Box

DEFAULT_BUILD_AREA = Box((0, 0, 0), (255, 255, 255))

editor = Editor(buffering=True, caching=True)
buildArea = editor.setBuildArea(DEFAULT_BUILD_AREA)
worldSlice = editor.loadWorldSlice(buildArea.toRect(), cache=True)

def setBuildArea(box: Box):
    global buildArea
    buildArea = editor.setBuildArea(box)
    global worldSlice
    worldSlice = editor.loadWorldSlice(box.toRect(), cache=True)
