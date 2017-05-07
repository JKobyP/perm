from functools import reduce

class Graph(object):
    def __init__(self, nodes={}, directed=False):
        self.Nodes = nodes
        self.numNodes = len(nodes)
        self.directed = directed
        self.numEdges = 0
        if len(nodes) != 0:
            self.numEdges = reduce(lambda x,y: x+y,map(lambda n:
                len(n.edges),nodes.values()))
        if not self.directed:
            if self.numEdges % 2 != 0:
                raise Error()
            self.numEdges = int(self.numEdges/2)

    # takes a key, returns the created node
    def add_node(self, k):
        if k not in self.Nodes:
            self.Nodes[k] = Node(k)
            self.numNodes = self.numNodes + 1
        return self.Nodes[k]

    # takes two keys and an optional weight
    def add_edge(self, frm, to, w=1):
        if frm == to:
            return
        if frm not in self.Nodes:
            self.add_node(frm)
        if to not in self.Nodes:
            self.add_node(to)
        self.Nodes[frm].addNeighbor(self.Nodes[to], w=w)
        self.numEdges = self.numEdges + 1
        if not self.directed:
            self.Nodes[to].addNeighbor(self.Nodes[frm], w=w)

    def has_edge(self, frm, to):
        return to in list(map(lambda n: n.key,self.Nodes[frm].getNeighbors()))

    def __contains__(self, key):
        return key in self.Nodes

    def getLabels(self):
        return list(randgraph.Nodes.keys)

    def getEdges(self):
        l= list(map(lambda n: n.edges, self.Nodes.values()))
        return [item for sublist in l for item in sublist]

    # node should be of Node type
    def __getitem__(self, node):
        return self.Nodes[node.key]

    def copy(self):
        g = Graph()
        g.Nodes = self.Nodes.copy()
        g.numNodes = self.numNodes
        g.numEdges = self.numEdges
        g.directed = self.directed
        return g

class Node(object):
    def __init__(self, key):
        self.key = key
        self.edges = []
    def addNeighbor(self, n, w=1):
        e = Edge(self, n,w=w)
        self.edges.append(e)
        return e
    def getNeighbors(self):
        neighbors = []
        for e in self.edges:
            neighbors.append(e.to)
        return neighbors
    def __str__(self):
        return str(self.key)
    def __repr__(self):
        return str(self)

class Edge(object):
    def __init__(self, frm, to, w=1):
        self.frm = frm
        self.to = to
        self.weight = w
