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
        self.edges = {}

    def __str__(self):
        return "Node \"%s\" with neighbours: %s" % (self.identifier, self.neighbours)
    
class Edge(object):
    """ Edge object initialized with an identifier, start and end Node object.
    """
    def __init__(self, identifier, start, end, isDirected=False):
        self.identifier = identifier
        self.start = start
        self.end = end
        if isDirected is None:
            """Reset argument in case multiple objects are initaliezed
            """
            isDireced = False
        self.isDirected = isDirected

    def __str__(self):
        return "Edge with identifier \"%s\"" % self.identifier

class SimpleGraph(object):
    """ Simple graph with a dictionary consisting of Node objects which
    are part of the graph. The Graph object is thought to be an input
    to a graph algorithm.
    """
    
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def __str__(self):
        return "Graph object with nodes: %s" % self.nodes.keys()

    def addNode(self, node):
        """ Add a node to the Graph object.
        """
        self.nodes[node.identifier] = node

    def addEdge(self, start, end, weight=1, directed=False):
        """ Add an edge to the Graph object. Opionally indicate the weight or cost and
        the direction of the edge.
            start: Node object representing the start of the edge
            end: Node object representing the end of the edge
            weight: length, cost or something else representing the weight of the edge
            directed: True if the edge can only be traversed from start to end 
        """
        if weight is None or weight is '':
            weight = 1
        if directed is None:
            directed = False
        if start.identifier not in self.nodes:
            return "Couldn't add Edge. Node %s not part of the graph." % start.identifier
        if end.identifier not in self.nodes:
            return "Couldn't add Edge. Node %s not part of the graph." % end.identifier
        if end.identifier not in start.neighbours:
            start.neighbours[end.identifier] = weight
            newEdge = Edge(str(start.identifier + end.identifier + str(weight)), start, end)
            if not directed and start.identifier not in end.neighbours:
                end.neighbours[start.identifier] = weight
                self.edges[newEdge.identifier] = newEdge
            else:
                newEdge.isDirected = True
                self.edges[newEdge.identifier] = newEdge
            start.edges[newEdge.identifier] = newEdge
            end.edges[newEdge.identifier] = newEdge
            return "Edge between %s and %s successfully added to graph." % (start.identifier, end.identifier)
        return "There is already an edge between %s and %s." % (start.identifier, end.identifier)

    def removeEdge(self, start, end, directed=False):
        """ Remove an edge between two nodes. Optionally indicate wether the edge is directed.
        """
        """ Prelimary variable definitions """
        startId = start.identifier
        endId = end.identifier
        weight = str(start.neighbours[endId])
        edgeId = str(startId + endId + weight)

        if self.edges[edgeId].isDirected != directed:
            """ Assure the edge to be removed has the direction indicated in
            the function call.
            """
            print("Couldn't remove Edge object. The direction indicated doesn't match the edge's direction")
            #raise ValueError("direction error"); instead exit funciton:
            return
        
        del self.nodes[startId].neighbours[endId] # unlink end from start
        del start.edges[edgeId] # remove reference to edge from start Node
        if not directed:
            del self.nodes[endId].neighbours[startId] # unlink start from end
            del end.edges[edgeId] # remove reference to edge from end Node
        del self.edges[edgeId] # remove reference to edge from Graph
        """ Delete the references to the Edge object, checking for direction.
        """

    def printAdjacencyList(self):
        for n in self.nodes.values():
            print("%s: %s" % (n.identifier, [str(i) for i in n.neighbours.keys()]))

class GraphRelations(object):
    """ Class to define the relation between two graphs.
    """
    def __init__(self): 
        pass

def relateGraphs(graph1, graph2, relation):
    """ Function to actually set the relation of two graphs. Makes
    use of the GraphRelation object.
    """
    pass


""" This section is used to define algorithms
"""

def diffColorNeighbours(graph, start):
    """ Graph algorithem: applies different colors to neighbours. Takes Graph object
    and starting Node object as arguments.
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
    g.addEdge(E,D)
    g.addEdge(E,G)
    g.addEdge(D,F)
    g.addEdge(G,F)

    g.printAdjacencyList()
    print("")
    print(g.edges)
    print("")
    print(g.nodes)
    print("")

    diffColorNeighbours(g, A)
    print("")
    diffColorNeighbours(g, E)
    
