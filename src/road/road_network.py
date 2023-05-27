from typing import Generic, TypeVar, Callable

T = TypeVar('T')


class RoadNode(Generic[T]):
    def __init__(self, val: T, hashfunc: Callable[[object], int] = hash):
        self._val = val
        self._hashfunc = hashfunc

    def __str__(self) -> str:
        return f"RoadNode({self.val})"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return self._hashfunc(self.val)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, RoadNode):
            return False
        return self.val == o.val

    @property
    def val(self):
        return self._val


class RoadEdge(Generic[T]):
    def __init__(self, path: list[RoadNode[T]] = []):
        self._path = [node for node in path]
        self._nodes = set(self._path)

    def __str__(self) -> str:
        return str(self._path)

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self._path)

    def __hash__(self) -> int:
        return hash((self.node1, self.node2))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, RoadEdge):
            return False
        return self.node1 == o.node1 and self.node2 == o.node2

    def __contains__(self, node: RoadNode[T]) -> bool:
        return node in self._nodes

    @property
    def path(self) -> list[RoadNode[T]]:
        return self._path

    @property
    def node1(self) -> RoadNode[T]:
        return self._path[0]

    @property
    def node2(self) -> RoadNode[T]:
        return self._path[-1]

    def split(self, node) -> tuple['RoadEdge[T]', 'RoadEdge[T]']:
        idx = self._path.index(node)
        return RoadEdge(self._path[:idx+1]), RoadEdge(self._path[idx:])

    def reverse(self) -> 'RoadEdge[T]':
        return RoadEdge(self._path[::-1])


class RoadNetwork(Generic[T]):
    def __init__(self, hotThreshold: int = 10):
        """A graph of RoadNodes and RoadEdges. The graph is undirected, and edges are bidirectional."""
        self._adj = dict[RoadNode[T], set[RoadEdge[T]]]()
        self._hotness = dict[RoadNode[T], int]()
        self._hotThreshold = hotThreshold

    def __str__(self) -> str:
        return str(self._adj)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def subnodes(self):
        """Returns an iterator over all subnodes in the graph. Subnodes are nodes that are contained in an edge."""
        return self._hotness.keys()

    @property
    def nodes(self):
        """Returns an iterator over all main nodes in the graph."""
        return self._adj.keys()

    @property
    def edges(self):
        """Returns an iterator over all edges in the graph."""
        for edges in self._adj.values():
            yield from edges

    @property
    def hotspots(self):
        """Returns an iterator over all hotspots in the graph. Hotspots are nodes with a hotness above the hotThreshold."""
        for node in self._hotness:
            if self.isHotspot(node):
                yield node

    def hotness(self, node: RoadNode[T]) -> int:
        """Returns the hotness of a node. Hotness is the number of edges that contain the node."""
        return self._hotness[node]

    def isHotspot(self, node: RoadNode[T]) -> bool:
        """Returns whether a node is a hotspot."""
        return self._hotness[node] >= self._hotThreshold

    def updateHotspots(self):
        """Updates the hotspots in the graph."""
        edges = set(self.edges)
        toUpgrade = set()
        toDowngrade = set()

        # Find nodes to upgrade and downgrade
        for node in self._hotness:
            if self.isHotspot(node) and node not in self._adj:
                toUpgrade.add(node)
            elif not self.isHotspot(node) and node in self._adj:
                toDowngrade.add(node)

        # upgrade nodes
        for node in toUpgrade:
            for edge in edges:
                if node in edge:
                    self.removeEdge(edge, updateHotspots=False)
                    edge1, edge2 = edge.split(node)
                    self.addEdge(edge1, updateHotspots=False)
                    self.addEdge(edge2, updateHotspots=False)

        # downgrade nodes
        for node in toDowngrade:
            self.removeNode(node, updateHotspots=False)

    def addNode(self, node: RoadNode[T]):
        """Adds a node to the graph."""
        self._adj.setdefault(node, set())

    def addEdge(self, edge: RoadEdge[T], updateHotspots: bool = True):
        """Adds an edge to the graph."""
        self._adj.setdefault(edge.node1, set()).add(edge)
        self._adj.setdefault(edge.node2, set()).add(edge.reverse())

        for node in edge.path:
            # update hotness
            self._hotness.setdefault(node, 0)
            self._hotness[node] += 1

        if updateHotspots:
            self.updateHotspots()

    def removeNode(self, node: RoadNode[T], updateHotspots: bool = True):
        """Removes a node from the graph."""
        if node not in self._adj:
            return

        for edge in self._adj[node]:
            self._adj[edge.node1].remove(edge)
            self._adj[edge.node2].remove(edge.reverse())

            for node in edge.path:
                # update hotness
                self._hotness[node] -= 1

                if self._hotness[node] == 0:
                    del self._hotness[node]

        del self._adj[node]

        if updateHotspots:
            self.updateHotspots()

    def removeEdge(self, edge: RoadEdge[T], updateHotspots: bool = True):
        """Removes an edge from the graph."""
        if edge.node1 not in self._adj[edge.node1] or edge.node2 not in self._adj[edge.node2]:
            return

        self._adj[edge.node1].remove(edge)
        self._adj[edge.node2].remove(edge.reverse())

        for node in edge.path:
            # update hotness
            self._hotness[node] -= 1

            if self._hotness[node] == 0:
                del self._hotness[node]

        if updateHotspots:
            self.updateHotspots()

    def neighbors(self, node: RoadNode[T]):
        """Returns an iterator over all neighbors of a node."""
        yield from (edge.node2 for edge in self._adj[node])

    def edge(self, node1: RoadNode[T], node2: RoadNode[T]) -> RoadEdge[T] | None:
        """Returns the edge between two nodes, or None if there is no edge between them."""
        for edge in self._adj[node1]:
            if edge.node2 == node2:
                return edge
        return None

