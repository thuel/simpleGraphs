#!/usr/bin/env python

"""Simple graph library with class definitions of Graph, Node and
Edge objects to be used in graph algorithmes.
"""

#import essential modules, libraries and methods/functions
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
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

class SimpleGraph(object):
    """ Simple graph with dictionary consisting of Node objects which
    are part of the graph. The Graph object is thought to be an input
    to a graph algorithem.
    """
    def __init__(self):
        self.nodes = {}

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

    def printAdjacencyList(self):
        for n in self.nodes.values():
            print("%s: %s" % (n.identifier, [str(i) for i in n.neighbours.keys()]))

def diffColorNeighbours(graph, start):
    """ Function to apply different colors to neighbours.
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

    diffColorNeighbours(g, A)

    diffColorNeighbours(g, E)
    
