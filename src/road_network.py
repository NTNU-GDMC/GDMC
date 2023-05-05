class RoadNode(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()


class RoadEdge(object):
    def __init__(self, path: list[tuple[int, int]] = []):
        self.path = [RoadNode(x, y) for x, y in path]

    def Node1(self):
        return self.path[0]

    def Node2(self):
        return self.path[-1]

    def len(self):
        return len(self.path)

    def __str__(self) -> str:
        return str(self.path)

    def __repr__(self) -> str:
        return self.__str__()


class RoadNetwork(object):
    def __init__(self, nodes: list[RoadNode], edges: list[RoadEdge]):
        self.nodes = nodes
        self.edges = edges

    def getEdge(self, node1, node2):
        for edge in self.edges:
            if edge.Node1() == node1 and edge.Node2() == node2:
                return edge
        return None

    def getEdgesByNode(self, node):
        for edge in self.edges:
            if edge.Node1() == node or edge.Node2() == node:
                yield edge

    def getEdgesByNodes(self, node1, node2):
        for edge in self.edges:
            if edge.Node1() == node1 and edge.Node2() == node2:
                yield edge

    def getEdgesByNode1(self, node1):
        for edge in self.edges:
            if edge.Node1() == node1:
                yield edge

    def getEdgesByNode2(self, node2):
        for edge in self.edges:
            if edge.Node2() == node2:
                yield edge
