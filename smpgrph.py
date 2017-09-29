#!/usr/bin/env python

"""Simple graph library with class definitions of Graph and Node objects to be
used in graph algorithmes. Edges are determined in a Graph object by setting
two Node objects of the Graph's nodes dictionary in relation to each other.
This is done by specifying the "weight" and optionaly the direction between
the two nodes in the neighbours dictionary of each Node object. The neighbouring
Node's identifier is the key while the "weight" is the value. When edges have no
direction the same "weight" is used for both Nodes.
"""

#import essential modules, libraries and methods/functions
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
""" To install builtins simply navigate to the package future and type "setup.py install"
into the command line.
"""
from priodict import priorityDictionary

"""Define classes of this library
"""

class Node(object):
    """ Node object initialized with an identifier. The Node object has
    dictionary called "neighbours" in which the neighbouring nodes in a
    graph will be stored. The identifier of the neighbour is the key, the
    weight or cost of the edge connecting the Node with neighbour is the
    value.
    """
    def __init__(self, identifier):
        self.identifier = identifier
        self.neighbours = {}

    def __str__(self):
        return "Node \"%s\" with neighbours: %s" % (self.identifier, self.neighbours)
    
class Edge(object):
    """ Edge object initialized with an identifier.
    """
    def __init__(self, identifier):
        self.identifier = identifier

    def __str__(self):
        return "Edge with identifier \"%s\"" % self.identifier

class SimpleGraph(object):
    """ Simple graph with a dictionary consisting of Node objects which
    are part of the graph. The Graph object is thought to be an input
    to a graph algorithm.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = self.getEdges() #doesn't work (to fix)

    def __str__(self):
        return "Graph object with nodes: %s" % self.nodes.keys()

    def addNode(self, node):
        """ Add a node to the Graph object.
        """
        self.nodes[node.identifier] = node

    def addEdge(self, start, end, weight=1, directed=False):
        """ Add an edge to the Graph object. Opionally indicate the weight or cost and
        the direction of the edge.
        """
        if start.identifier not in self.nodes:
            return "Couldn't add Edge. Node %s not part of the graph." % start.identifier
        if end.identifier not in self.nodes:
            return "Couldn't add Edge. Node %s not part of the graph." % end.identifier
        if end.identifier not in self.nodes[start.identifier].neighbours:
            self.nodes[start.identifier].neighbours[end.identifier] = weight
            if not directed and start.identifier not in self.nodes[end.identifier].neighbours:
                self.nodes[end.identifier].neighbours[start.identifier] = weight
            return "Edge between %s and %s successfully added to graph." % (start.identifier, end.identifier)
        return "There is already an edge between %s and %s." % (start.identifier, end.identifier)

    def removeEdge(self, start, end, directed=False):
        """ Remove an edge between two nodes. Optionally indicate wether the edge is directed.
        """
        del self.nodes[start.identifier].neighbours[end.identifier]
        if not directed:
            del self.nodes[end.identifier].neighbours[start.identifier]

    def getEdges(self):
        """ Return a list of Edge objects which form the graph.
        Returns every edge two times allthought the weight ist the same (to fix).
        """
        lst = []
        for node in self.nodes.values():
            for neighbour, weight in node.neighbours.items():
                edge = str(node.identifier + neighbour + str(weight))
                print(edge)
                if edge not in self.edges:
                    lst.append(edge)
        print(lst)
        return lst

    def printAdjacencyList(self):
        for n in self.nodes.values():
            print("%s: %s" % (n.identifier, [str(i) for i in n.neighbours.keys()]))

class GraphRelation(object):
    """ Class to define the relation between to graphs.
    """
    pass

def relateGraphs(graph1, graph2, relation):
    """ Function to actually set the relation of two graphs. Makes
    use of the GraphRelation object.
    """
    pass


""" This section is used to define algorithms
"""

def diffColorNeighbours(graph, start):
    """ Graph algorithem: applies different colors to neighbours.
    """
    def initDiffColorNeighbours(g, colors):
        """ Subfunction to initialize the graph for calculation of different colors
        of the neighbours.
        """
        colors.extend(["red", "blue", "green", "yellow", "brown", "black", "cyan"])
        for n in g.nodes.values():
            n.visited = False
            n.distance = float('inf')
            n.color = None

    def updateQueue(g, queue, node):
        """ Subfunction to update the queue with the neighbours of the node in a graph. Check
        if neighbours are already visited.
        """
        d = g.nodes
        queue.extend([d[i].identifier for i in node.neighbours.keys() if not d[i].visited and d[i].identifier not in queue])
        
    def printDiffColors(g):
        """ Print the result of the algorithem for the given graph.
        """
        nodeList = sorted(g.nodes.keys())
        d = g.nodes
        for n in nodeList:
            print("Node: %s\t\tColor: %s\tN. colors: %s" % (d[n].identifier, d[n].color, [str(g.nodes[i].color) for i in d[n].neighbours]))
    colors = []
    initDiffColorNeighbours(graph, colors)

    queue = [start.identifier]
    while len(queue) > 0:
        """ The actual algorithm. Takes the first node in the queue, marks
        it as visited, checks which colors are already applied to the
        neighbours of the node, assigns the first color of the residual
        color list to the node, updates the queue and finally removes the
        actual node from the queue, to start the whole processes with the
        next node in the queue.
        """
        node = graph.nodes[queue[0]]
        node.visited = True

        n_colors = [graph.nodes[i].color for i in node.neighbours]
        node.color = list(set(colors).difference(n_colors))[0]
        
        updateQueue(graph, queue, node)
        queue = queue[1:]

    printDiffColors(graph)


    
if __name__ == "__main__":
    A = Node("A")
    B = Node("B")
    C = Node("C")
    D = Node("D")
    E = Node("E")
    F = Node("F")
    G = Node("G")
    g = SimpleGraph()
    g.addNode(A)
    g.addNode(B)
    g.addNode(C)
    g.addNode(D)
    g.addNode(E)
    g.addNode(F)
    g.addNode(G)
    g.addEdge(A,C)
    g.addEdge(A,B)
    g.addEdge(A,E)
    g.addEdge(B,E)
    g.addEdge(B,D)
    g.addEdge(B,A)
    g.addEdge(E,D)
    g.addEdge(E,G)
    g.addEdge(D,F)
    g.addEdge(G,F)

    g.printAdjacencyList()
    print("")
    print(g.edges)
    g.edges=g.getEdges()
    print(g.edges)
    print("")

    diffColorNeighbours(g, A)

    diffColorNeighbours(g, E)
    
