from gdpc import Editor
from gdpc.vector_tools import Box

DEFAULT_BUILD_AREA = Box((0, 0, 0), (255, 255, 255))

editor = Editor(buffering=True, caching=True)
editor.setBuildArea(DEFAULT_BUILD_AREA)
editor.loadWorldSlice(DEFAULT_BUILD_AREA.toRect(), cache=True)
