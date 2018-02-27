#!/usr/bin/env python

"""Simple graph library with class definitions of Graph and Node
objects to be used in graph algorithms. Edges are determined in
a Graph object by setting two Node objects of the Graph's nodes
dictionary in relation to each other. This is done by specifying
the "weight" and optionaly the direction between the two nodes in
the neighbours dictionary of each Node object. The neighbouring
Node's identifier is the key while the "weight" is the value. When
edges have no direction the same "weight" is used for both Nodes.
"""

#import essential modules, libraries and methods/functions
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
# To install builtins on windows: simply navigate to the
# package future and type "setup.py install into the command line."
from builtins import *
import math
import random
import os

from priodict import priorityDictionary

#######################################################################
# Define classes of this library

class Table(object):
    """ Class to create a table with from a list of lists.

    Initialises with a data list and optionally with a list of
    header fields.

    data_list: a list with the rows of the table, each row itself a
      list of values.
    has_headers: boolean to indicate if data_list contains a header row
      as first list item.
    """
    def __init__(self, data_list, has_headers=False):
        def setupTable(self, data_list):
            """ Convert the data List to dictionary of table cells.
            The data_list is a list of list(s).
            """
            self.headers = []
            if has_headers:
                for col in range(self.numColumns):
                    self.headers.append(data_list[col][0])
                    del data_list[col][0]
                self.numRows -= 1
            else:
                divider = math.ceil(self.numColumns/26)
                for i in range(divider):
                    first = ""
                    if i > 0:
                        first = chr(i+65)
                    for col in range(self.numColumns):
                        self.headers.append(first+chr(col+65))
            data = {}
            for col in range(self.numColumns):
                for row in range(self.numRows):
                    cellId = u"c" + str(col) + u"r" + str(row)
                    data[cellId] = data_list[col][row]
            return data

        self.numColumns = len(data_list)
        self.numRows = len(data_list[0])
        self.data = setupTable(self, data_list)

    def printTable(self):
        """ Print out the table.
        """
        border = 3 # spacing + 1
        columnWidths = self.getColumnWidths()
        tableWidth = sum(columnWidths)+(border * self.numColumns) +1
        print("="*tableWidth)
        header = "|"
        for col in range(self.numColumns):
            header += " " * int(math.floor(border/3)) + str(self.headers[col])
            header += " "*(columnWidths[col] - len(self.headers[col])) +" |"
        print(header)
        print("="*tableWidth)

        if self.data == {}:
            return
        else:
            for row in range(self.numRows):
                pRow = "|"
                columnValues = self.getValuesFromRow(row)
                for cell in range(len(columnValues)):
                    pRow += " " + columnValues[cell]
                                + " "*(columnWidths[cell]
                                - len(columnValues[cell])) +" |"
                print(pRow)
                print("-"*tableWidth)

    def getValuesFromColumn(self, col):
        """ Returns a list of the values in column col.
        """
        values = []
        for row in range(self.numRows):
            cellId = cellId = "c" + str(col) + "r" + str(row)
            values.append(self.data[cellId])
        return values

    def getValuesFromRow(self, row):
        """ Returns a list of the values in row row.
        """
        values = []
        for col in range(self.numColumns):
            cellId = cellId = "c" + str(col) + "r" + str(row)
            values.append(self.data[cellId])
        return values

    def getColumnWidths(self):
        """ Returns a list with the column width of the longest data
        field in every column.
        """
        columnWidths = []
        for col in range(self.numColumns):
            if self.data == {}:
                columnWidths.append(len(self.headers[col]))
            else:
                columnWidths.append(max(len(max(
                        self.getValuesFromColumn(col), key=len)),
                                        len(self.headers[col])))
        return columnWidths

class AttributeTable(Table):
    """ Class of a special table with a given number of columns with
    given column headers. Used to give an overview of the attributes
    to assign to the Node and Edge objects of a graph object. The
    object is used to init a Graph object with further functionality.
    """
    def __init__(self, data_list=[[]]):
        def setupTable(self, data_list):
            """ Convert the data List to dictionary of table cells.
            The data_list is a list of list(s).
            """
            self.headers = ["Name", "Networkcontext", "Type", "Computed"]
            data = {}
            for col in range(self.numColumns):
                for row in range(self.numRows):
                    cellId = "c" + str(col) + "r" + str(row)
                    data[cellId] = data_list[col][row]
            return data

        if len(data_list) > 4:
            print("Too many columns in data_list")
            return
        self.numColumns = 4
        self.numRows = len(data_list[0])
        self.data = setupTable(self, data_list)

class SetupRoutinesTable(Table):
    """ Class of a special table with a given number of columns with
    given column headers. Used to give an overview of the attributes
    the Node and Edge objects of a graph object. The object is used
    to init a Graph object with further functionality.
    """
    def __init__(self, data_list=[[]]):
        def setupTable(self, data_list):
            """ Convert the data List to dictionary of table cells.
            The data_list is a list of list(s).
            """
            self.headers = ["Field", "Formulae", "Comment"]
            # Where Field is either Node, Edge or a variable
            # definition starting with a dollar sign.
            data = {}
            for col in range(self.numColumns):
                for row in range(self.numRows):
                    cellId = "c" + str(col) + "r" + str(row)
                    data[cellId] = data_list[col][row]
            return data

        if len(data_list) > 3:
            print("Too many columns in data_list")
            return
        self.numColumns = 3
        self.numRows = len(data_list[0])
        self.data = setupTable(self, data_list)

class Node(object):
    """ Node object for use with a graph object.

    The Node object is initialised with an identifier. It contains a
    dictionary called "neighbours" in which the neighbouring nodes in a
    graph will be stored. The identifier of the neighbour is the key,
    the weight or cost of the edge connecting the Node with neighbour
    is the value.

    identifier: string identifying the Node object.
    neighbours: dict of neighbouring Node objects.
    edges: dict with Edge objects connecting the Node object to its
      neighbours.
    """
    def __init__(self, identifier):
        self.identifier = identifier
        self.neighbours = {}
        self.edges = {}

    def __str__(self):
        return "Node \"%s\" with neighbours: %s" % (self.identifier,
                                                    self.neighbours)

class Edge(object):
    """ Edge object for use with graph object.

    The Edge object is initialised with an identifier, a start and an
    end Node object. Direction and weight of the edge in the graph may
    be provided optionally.

    identifier: string identifying the Edge object.
    start: Node object representing the start of the Edge object.
    end: Node object representing the end of the Edge object.
    is_directed: boolean to indicate if the edge is directed.
    weight: weight of the edge in the graph. E.g. distance or cost.
    """
    def __init__(self, identifier, start, end, is_directed=False, weight=1):
        self.identifier = identifier
        self.start = start
        self.end = end
        if is_directed is None:
            """Reset argument in case multiple objects are initaliezed
            """
            isDireced = False
        self.is_directed = is_directed

    def __str__(self):
        return "Edge with identifier \"%s\"" % self.identifier

class Simplegraph(object):
    """ Simple graph object to calculate graph algorithms with.

    Initialised with the optional arguments attributes and
    setup_routines. The Simplegraph object contains a dict of Node
    objects which are part of the graph and a dict of Edge objects
    connecting the Node objects.

    attributes: AttributeTable object containing information on the
      attributes to be added to Node and Graph objects.
    setup_routines: a SetupRoutinesTable object containing the routines
      to setup up the graph object, i.e. to populate it with Node and
      Edge objects.
    nodes: dict of Node objects belonging to the Simplegraph object.
    edges: dict of Edge objects belonging to the Simplegraph object.
    """
    def __init__(self, attributes=AttributeTable(data_list = [[]]),
                 setup_routines = SetupRoutinesTable(data_list = [[]])):
        self.nodes = {}
        self.edges = {}
        if attributes is None:
            attributes = Table(data_list = [[]])
        self.attributes = attributes
        if setup_routines is None:
            setup_routines = Table(data_list = [[]])
        self.setup_routines = setup_routines

    def __str__(self):
        return "Graph object with nodes: %s" % self.nodes.keys()

    def add_node(self, node):
        """ Add a node to the Graph object.

        node: node object to be added.
        """
        if not isinstance(node, Node):
            raise(ValueError, "Argument needs to be a node object.")
        if node.identifier in self.nodes:
            print("Node %s already in graph. Skipping."
                  % node.identifier)
            return
        self.nodes[node.identifier] = node

    def add_edge(self, start, end, weight=1, directed=False):
        """ Add an edge to the Graph object.

        Opionally indicate the weight or cost and the direction of the
        edge.

        start: Node object representing the start of the edge or the
          identifier of an Node object as string
        end: Node object representing the end of the edge or the
          identifier of an Node object as string
        weight: length, cost or something else representing the weight
          of the edge
        directed: True if the edge can only be traversed from start to
          end
        """
        # Test needed in case the function is called as add_edge("A", "B")
        # instead of add_edge(u"A", u"B") in version 2.7.
        try:
            start = start.decode("utf-8")
        except:
            start = start
        # Further tests ensuring compatibility between python versions and
        # to ensure objects of the right type are provided.
        try:
            basestring
        except NameError:
            basestring = str
        if (not isinstance(start, Node) and not isinstance(start, basestring)
                and not isinstance(start, int)):
            print("Argument start is of wrong type. Use Node, str or int.")
            return
        if (not isinstance(end, Node) and not isinstance(end, basestring)
                and not isinstance(end, int)):
            print("Argument end is of wrong type. Use Node, str or int.")
            return
        # Reset weight and directed in case no argument is provided and
        # the function was called with arguments before.
        if weight is None or weight is '':
            weight = 1
        if directed is None:
            directed = False

        if isinstance(start, basestring) or isinstance(start, int):
            start = Node(start)
            self.add_node(start)
        if isinstance(end, basestring) or isinstance(end, int):
            end = Node(end)
            self.add_node(end)
        # Ensure start and end are in the Graph object in case their
        # given as Node objects.
        if not self.is_in_graph(start):
            print("Couldn't add Edge. Node %s not part of the graph."
                  % start.identifier)
            return
        if not self.is_in_graph(end):
            print("Couldn't add Edge. Node %s not part of the graph."
                  % end.identifier)
            return

        if end.identifier not in start.neighbours:
            start.neighbours[end.identifier] = weight
            newEdge = Edge(str(start.identifier + end.identifier
                               + str(weight)), start, end)
            if not directed and start.identifier not in end.neighbours:
                end.neighbours[start.identifier] = weight
                self.edges[newEdge.identifier] = newEdge
            else:
                newEdge.is_directed = True
                self.edges[newEdge.identifier] = newEdge
            start.edges[newEdge.identifier] = newEdge
            end.edges[newEdge.identifier] = newEdge
            return "Edge between %s and %s successfully added to graph." % (
                start.identifier, end.identifier)
        return "There is already an edge between %s and %s." % (
            start.identifier, end.identifier)

    def remove_edge(self, start, end, directed=False):
        """ Remove an edge between two nodes.

        Optionally indicate whether the edge is directed or not.
        Default is directed.

        start: starting Node of the edge to be removed.
        end: ending Node of the edge to removed.
        directed: boolean to indicate whether the Edge has a direction
          or not.

        """
        # Prelimary variable definitions
        startId = start.identifier
        endId = end.identifier
        weight = str(start.neighbours[endId])
        edgeId = str(startId + endId + weight)

        # Assure the edge to be removed has the direction indicated in
        # the function call.
        if self.edges[edgeId].is_directed != directed:
            print("Couldn't remove Edge object. The direction indicated
                  doesn't match the edge's direction")
            #TODO:raise ValueError("direction error"); instead of return
            return

        del self.nodes[startId].neighbours[endId] # unlink end from start
        del start.edges[edgeId] # remove reference to edge from start Node
        if not directed:
            del self.nodes[endId].neighbours[startId] # unlink start from end
            del end.edges[edgeId] # remove reference to edge from end Node
        del self.edges[edgeId] # remove reference to edge from Graph

    def is_in_graph(self, node_or_edge):
        """ Returns True if Node or Edge object is part of the graph.

        Check whether a Node or Edge object provided as argument is part
        of the Graph object.

        node_or_edge: Node or Edge object to check for graph membership
        """
        if isinstance(node_or_edge, Node):
            return node_or_edge.identifier in self.nodes
        elif isinstance(node_or_edge, Edge):
            return node_or_edge.identifier in self.edges
        else:
            print("Wrong type provided. Use Node or Edge object as argument.")

    def print_adjacencylist(self):
        for n in self.nodes.values():
            print("%s: %s" % (n.identifier,
                              [str(i) for i in n.neighbours.keys()]))

    def print_edges(self):
        edgeList = list(sorted(self.edges.keys()))
        edges = dict(self.edges)
        tblEdges = Table([['Edge_ID']+[x for x in edgeList], \
                    ['Start']+[edges[x].start.identifier for x in edgeList],\
                    ['End']+[edges[x].end.identifier for x in edgeList]],
                    True)
        tblEdges.printTable()

class Graphrelation(object):
    """ Class to define the relation between two graphs.
    """
    def __init__(self):
        pass

""" Define functions and methods for this library
"""

def excel_to_table(excel_tbl, has_headers=True):
    """ Returns a Table object from a excel workbook with one sheet.

    Expects data to begin in top left cell of the first sheet.

    excel_tbl: path to the excel table to convert
    has_headers: boolean to indicate if excel table contains header
      information
    """
    from xlrd import open_workbook as openwb
    import os
    if has_headers is None:
        has_headers = True
    filename, ext = os.path.splitext(excel_tbl)
    if ext in ['xlsx', 'xls']:
        ext = ""
    else:
        ext = ".xlsx"
    try:
        wb = openwb(excel_tbl + ext)
    except:
        raise ValueError("file needs to be xlsx or path specified
                         including extension.")
    sheet = wb.sheets()[0]
    data_list = []
    for col in range(sheet.row_len(0)):
        data_list.append(sheet.col_values(col))
    return Table(data_list, has_headers)

def setup_graph(node_table, edge_table):
    """ Function to set up a Graph object.

    name: name of the Graph object
    node_table: a table of nodes (identifier needed, further attributes
      welcome)
    edge_table: a table of edges (identifier, start, end needed, weight
      and direction optional)
    """
    pass

def relate_graphs(graph1, graph2, relation):
    """ Function to actually set the relation of two graphs. Makes
    use of the GraphRelation object.
    """
    pass

def send_mail(sender, receiver, subject, message):
    """ Function to send mail.
    """
    import smtplib
    if type(receiver) is not type([]):
        raise ValueError("Receiver is a list of receivers.")
    receivers = ",".join(receiver)
    mail = "\r\n".join([
        "From: %s" % sender,
        "To: %s" % receivers,
        "Subject: %s" % subject,
        "",
        "%s" % message
        ])

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com:587')
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(sender, "mein.weihnachts.wichtler.mail.konto.sic!")
        smtpObj.sendmail(sender, receivers, mail)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email with receiver %s" % receivers)

def xmas_elves_mail(graph):
    """ Send E-Mails to persons taking part in X-mas elves arrangement

    Create e-mails for X-mas elves arrengement, where every person is
    the elf of another person making a present to this other person.
    Expects xmaselves() function to be run on graph before calling this
    function.

    graph: The Graph object of an xmaselves constallation which was
      solved with the xmaselves() algorithm before calling this
      function.
    """
    data = []
    for n in graph.nodes.values():
        subject = "Wichtel Auslosung"
        sender = "weihnachts.wichtler@gmail.com"
        receiver = [n.email]
        msg = "Hallo %s\n\nDu bist das Wichteli von %s.\n\n\
Lieber Gruss\n\nDer automatische Wichtler" % (n.identifier, n.presentee)
        # print(sender, receiver, subject, msg)
        send_mail(sender, receiver, subject, msg)

""" This section is used to define algorithms
"""

def diff_color_neighbours(graph, start, colors=[]):
    """ Applies different colors to neighbours in a graph.

    A graph algorithm taking a Graph object and a starting Node object
    as arguments. No neighbours get the same color applied to.

    grpah: the Simplegraph object with Nodes of all players and Edges
     representing a neighbour relationship.
    start: the Node object to begin the algorithm with.
    colors: a list of colors to color the Node objects with.
    """
    if colors is None:  # Reset colors
        colors=[]

    def init_dffclrnghbrs(g, colors):
        """ Initialize the graph for different color algorithm.

        Subfunction in the diff_color_neighbours algorithm. Initialising
        the graph with attributes visited, distance and color as well
        as the colors to be applied to the Node objects.

        g: Simplegraph object.
        colors: list of colors to use for coloring the the nodes
        """
        colors.extend(["red", "blue", "green", "yellow",
                       "brown", "black", "cyan"])
        for n in g.nodes.values():
            n.visited = False
            n.distance = float('inf')
            n.color = None

    def update_queue(g, queue, node):
        """ Update queue with the neighbours of a Node object.

        Subfunction in the diff_color_neighbours algorithm to update
        the queue with the neighbours of a given node in a graph.
        Checks if neighbours are already visited.

        g: graph running the algorithm on.
        queue: the queue with unvisited Node objects in the graph.
        node: the Node object whos neighbours get added to the queue
         if they are unvisited.
        """
        d = g.nodes
        queue.extend([d[i].identifier for i in node.neighbours.keys()
                      if not d[i].visited and d[i].identifier not in queue])

    def print_diff_colors(g):
        """ Print the result of the algorithm for the given graph.
        """
        nodeList = sorted(g.nodes.keys())
        d = g.nodes
        for n in nodeList:
            print("Node: %s\t\tColor: %s\tN. colors: %s"
                  % (d[n].identifier, d[n].color,
                     [str(g.nodes[i].color) for i in d[n].neighbours]))

    init_dffclrnghbrs(graph, colors)

    queue = [start.identifier]

    # The actual algorithm: Takes the first node in the queue,
    # marks it as visited, checks which colors are already applied
    # to the neighbours of the node, assigns the first color of the
    # residual color list to the node, updates the queue and
    # finally removes the actual node from the queue, to start the
    # whole processes with the next node in the queue.
    while len(queue) > 0:
        node = graph.nodes[queue[0]]
        node.visited = True

        n_colors = [graph.nodes[i].color for i in node.neighbours]
        node.color = list(set(colors).difference(n_colors))[0]

        update_queue(graph, queue, node)
        queue = queue[1:]

    print_diff_colors(graph)

def xmaselves(graph):
    """ Randomly assign each node to only one connected node.

    A grpah algorithm which randomly removes edges between nodes in a
    way that every node is connected to one node in the resulting graph
    only. The intended use case is to assign elves for X-mas.
    Returns a list of tuples: (elf, presentee, email).

    graph: the Simplegraph object to run the algorithm on.
    """

    def init_elves(graph):
        """ Initialise the graph for the problem to be solved.
        """
        for n in graph.nodes.values():
            n.visited = False
            n.distance = float('inf')
            n.presentee = None

    elves = graph.nodes.keys()
    init_elves(graph)
    d = dict(graph.nodes)
    queue = [random.choice(list(d))]
    while len(queue) > 0:
        node = d[queue[0]]
        node.visited = True
        try:
            node.presentee = random.choice(list(node.neighbours))
        except:
            node.presentee = ""
        for n in d.values():
            if n is not node:
                try:
                    graph.remove_edge(n, d[node.presentee],directed=True)
                except:
                    continue
        remove_list = [n for n in node.neighbours if n != node.presentee]
        for n in remove_list:
            try:
                graph.remove_edge(node, d[n], directed=True)
            except:
                print("couldn't remove %s from neighbours of %s"
                      % (n, node.identifier))
                continue
        min_presentees = float('inf')
        for n in d.values():
            min_presentees = min(len(n.neighbours), min_presentees)
        for n in d.values():
            if len(n.neighbours) == min_presentees and not n.visited:
                queue.append(n.identifier)
                break
        queue.extend([d[n].identifier for (n in d.keys()
                                           if not d[n].visited
                                           and d[n].identifier not in queue]))
        queue = queue[1:]
    for n in d.values():
        if n.presentee not in elves:
            raise ValueError("Run led to node with no neighbours.
                             Please reexecute.")


if __name__ == "__main__":
    A = Node("A")
    B = Node("B")
    C = Node("C")
    D = Node("D")
    E = Node("E")
    F = Node("F")
    G = Node("G")
    g = Simplegraph()
    g.add_node(A)
    g.add_node(B)
    g.add_node(C)
    g.add_node(D)
    g.add_node(E)
    g.add_node(F)
    g.add_node(G)
    g.add_edge(A,C)
    g.add_edge(A,B)
    g.add_edge(A,E)
    g.add_edge(B,E)
    g.add_edge(B,D)
    g.add_edge(E,D)
    g.add_edge(E,G)
    g.add_edge(D,F)
    g.add_edge(G,F)

    g.print_adjacencylist()
    print("")
    print(g.edges)
    print("")
    print(g.nodes)
    print("")

    diff_color_neighbours(g, A)
    print("")
    diff_color_neighbours(g, E)
    print("")
    print("With headers")
    tab = Table([['Colors', 'brown', 'green', 'brown', 'brown'],
                 ['Status', 'brown', 'green', 'brown', 'brown'],
                 ['Long Word', 'you thought?', 'no way baby!',
                  'yes, sir!', 'brown fox']
                ]
                , True)
    tab.printTable()
    print("")
    print("Without headers")
    tab2 = Table([['brown', 'green', 'brown', 'brown']], False)
    tab2.printTable()

    print('')
    g.print_edges()

    print('')
    newTab = excel_to_table(os.path.join(os.path.curdir,
                                         'inputtables', 'testtbl'))
    newTab.printTable()

    print('xmas elves starting here')
    xmasTab = excel_to_table(os.path.join(os.path.curdir,
                                          'inputtables', 'wichtel'))
    x = Simplegraph()
    for i in range(xmasTab.numRows):
        A = Node(xmasTab.getValuesFromColumn(0)[i])
        A.email = xmasTab.getValuesFromColumn(1)[i]
        A.partner = xmasTab.getValuesFromColumn(2)[i]
        x.add_node(A)
    elves = x.nodes.values()
    for elf in elves:
        for presentee in elves:
            if elf != presentee and presentee.identifier != elf.partner:
                x.add_edge(elf, presentee, directed=True)
    xmaselves(x)
    xmas_elves_mail(x)
    """for n in x.nodes.values():
        print("%s mit E-Mail %s ist Wichtel von %s."
        % (n.identifier, n.email, n.presentee))
    """
