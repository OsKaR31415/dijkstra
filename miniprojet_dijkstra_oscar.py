from collections import namedtuple

# Create a node object. Used in the dijksra algorithm.
Node = namedtuple("Node", ["name", "cost", "path_to"])


class Heap:
    """Implementation of a minimum heap.
    A minimum heap is a structure you can put values in, and get them back.
    It is called "minimum" because you get the minimum value each time.
    For this implementation, the values are *Node* objects, and the key for
    determination of the minimum is the *cost* attribute.
    """

    def __init__(self):
        """Create the Heap"""
        # initialise contents to an empty list
        self.__contents__ = list()

    def __bool__(self):
        """The boolean value of the heap.
        Answers the question "is the heap not empty ?".
        """
        return bool(self.__contents__)

    def __str__(self):
        """The string value of the heap.
        Returns the string "Heap(...)" , "..." being a list of *Node* objects
        reparated by ", " (their representations is called with *repr*)."""
        return "Heap(" + ", ".join(map(repr, self.__contents__)) + ")"

    def push(self, value):
        """Put a new value into the Heap."""
        self.__contents__.append(value)

    def top(self):
        """Returns the minimum value of the heap without removing it from the
        heap."""
        actual_min_value = float("inf")
        actual_min = None
        for elt in self.__contents__:
            if elt.cost < actual_min_value:
                actual_min_value = elt.cost
                actual_min = elt
        return actual_min

    def pop(self):
        """Returns the minimum value of the heap and remove it from the heap.
        funny to do some heap.pop() !!!"""
        self.__contents__.remove(top := self.top())
        return top


class Graph:
    """Object representing a graph
    """

    def __init__(self):
        """Initialise the Graph object."""
        self.__adj__ = dict()
        self.order = 0

    def __str__(self) -> str:
        """The string value of the Graph object."""
        return str(self.__adj__).replace("}, ", "},\n ")

    def exists_node(self, node) -> bool:
        """Tells if a given node exists in the graph.

        Args:
            node: The node to search.

        Returns:
            bool: True if *node* is in the graph, False else."""
        if self.__adj__.get(node) is None:
            return False
        return True

    def exists_link(self, node_start, node_end) -> bool:
        """Tells if 2 nodes (*node_start* and *node_end*) are linked in this
        way : node_start --> node_end.

        Args:
            node_start: The starting node of the link.
            node_end: The ending node if the link.

        Returns:
            bool: True if node_start --> node_end exists, False else.
            """
        if not self.exists_node(node_start):
            return False
        if not self.exists_node(node_end):
            return False
        return self.__adj__[node_start].get(node_end) is not None

    def add_node(self, node):
        """Add a node to the graph.
        """
        if self.exists_node(node):
            raise KeyError("You tried to add an existing node")
        self.__adj__[node] = dict()
        self.order += 1

    def add_link(self, node_start, node_end, weight: int or float = 1):
        """Add a link (one-way) to the graph.
        Adds nodes if they do not exist.

        Args:
            node_start: The starting node of the link.
            node_end: The ending node of the link.
            weight (optionnal, int or float): the weight of the link.
                Defaults to 1.
        """
        if not self.exists_node(node_start):
            self.add_node(node_start)
        if not self.exists_node(node_end):
            self.add_node(node_end)
        self.__adj__[node_start].update({node_end: weight})

    def add_symetric_link(self, node1, node2, weight: int or float = 1):
        """Add a symetric link (a --> b AND b --> a) to the graph.

        Args:
            node1 and node2: The nodes to add.
            weight (optionnal, int or float): the weight of the link.
                Defaults to 1.
            """
        self.add_link(node1, node2, weight)
        self.add_link(node2, node1, weight)

    def get_all_nodes(self) -> list:
        """Get a list of all the nodes of the graph.

        Reutrns:
            list: The list of the names of all the nodes of the graph."""
        return list(self.__adj__.keys())

    def get_neighnours(self, node) -> list:
        """Get all the neighbours of a given node.

        Args:
            node: The node to get neighbours of.

        Returns:
            list: The list of all neighbours of *node*"""
        if not self.exists_node(node):
            raise KeyError("This node does not exist")
        neighbours = list(self.__adj__[node].keys())
        return neighbours

    def get_neighnours_distances(self, node):
        """Get the distances to each neighbour of *node*.

        Args:
            node: The node to search the distances to each neighbour of.

        Returns:
            list: The list of the distances to each neighbour of *node*."""
        if not self.exists_node(node):
            raise KeyError("This node does not exist")
        neighbours = list(self.__adj__[node].values())
        return neighbours

    def get_weight(self, node_start, node_end) -> int or float:
        """Get the weight of a link.

        Args:
            node_start and node_end: The nodes of the link. The link is :
                node_start --> node_end.

        Returns:
            int or float: The weight of the link."""
        if not self.exists_link(node_start, node_end):
            raise KeyError("This link does not exist")
        return self.__adj__[node_start][node_end]

    def nearest_neighbour(self, node):
        """Returns the nearest neighbour of *node*.

        Args:
            node: The node to find the nearest neighbour of.

        Returns:
            the name of the nearest neighbour of *node*.
        """
        neighbours = set(self.get_neighnours(node))
        neighbours = neighbours - set(without)
        distances = list()
        for neighb in neighbours:
            distances.append([self.get_weight(node, neighb), neighb])
        return min(distances)[1]

    def dijkstra(self, node_start, node_end) -> tuple[int or float, list]:
        """Search the shortest distances and the matching path from *node_start*
        to *node_end*.
        This implementation uses the dijkstra algorithm, with a heap.

        Args:
            node_start and node_end: The starting and ending nodes. The
            algorithm searches the shortest path from node_start to node_end.

        Returns:
            tuple[int or float, tuple]: A tuple containing :
                0: The length of the shortest path.
                1: A tuple. listing the nodes of the path from *node_start* to
                    *node_end*."""
        ##### Implementation ###################################################
        # the algorithm works like so :                                        #
        #                                                                      #
        # 1. Stating with the first node (*node_start*) as the current node    #
        # 2. Put all the neighbours of the current node to the heap. Their     #
        #      *cost* attribute is increased of the cost of the current node,  #
        #      so it matches the shortest known distance.                      #
        # 3. Pop a node from the heap. The heap is a minimum heap, so it always#
        #      returns the element with le least cost.                         #
        # 4. Take this poped element is now used as the new current node.      #
        # 5. if the heap is empty, finish, else restart at 2.                  #
        #                                                                      #
        # This algorithm has a problem : if there is any cycle in the graph, it#
        # will never terminate. So we need to store which nodes we already     #
        # visited to skip them instead of always adding them to the heap.      #
        #                                                                      #
        # The next thing to add is the path finding : this simple version can  #
        # only get the shortest distance between 2 nodes, but not the matching #
        # path. So we will store the path to a node in the node himself : this #
        # is the attribute *path_to* of the *Node* object. The path is updated #
        # each time a shorter one is found (as the whole object is replaced by #
        # its version with a least cost).                                      #
        ########################################################################

        # initialize a heap with the starting node
        heap = Heap()
        heap.push(Node(node_start, 0, path_to=()))

        # initialize the set of already seen nodes
        seen = set()
        # initialize the set of minimum known distances
        minimums = {node_start: 0}

        # while the heap is not empty
        while heap:
            # get the nearest node (an object of the class Node)
            nearest_node = heap.pop()
            # Get the cost, the name and the path to this node
            cost = nearest_node.cost
            current_node = nearest_node.name
            path = nearest_node.path_to

            # if this node is already seen, skip it
            if current_node not in seen:
                # this node is now seen
                seen.add(current_node)
                # append to the shortest path
                path += (current_node,)
                # if the path is complete, stop and return it
                if current_node == node_end:
                    return (cost, path)

                # iterate over each neighbour of *current_node* and its distance
                # from *current_node*
                for current_cost, neighbour in zip(
                        self.get_neighnours_distances(current_node),
                        self.get_neighnours(current_node)):
                    # if the neighbour is already seen, skip it
                    if neighbour in seen:
                        continue
                    # get the previous minimum distance to *current_node*
                    previous = minimums.get(neighbour)
                    # get the current distance to *current_node*
                    next = cost + current_cost
                    # get the minimum between both
                    if previous is None or next < previous:
                        minimums[neighbour] = next
                        # push this minimum into the heap
                        heap.push(Node(neighbour, next, path_to=path))

        # if no path is found, return these values :
        return float("inf"), None


if __name__ == "__main__":
    graph_1 = Graph()
    graph_1.add_symetric_link(1, 2, weight=10)
    graph_1.add_symetric_link(1, 3, weight=7)
    graph_1.add_symetric_link(1, 4, weight=200)
    graph_1.add_symetric_link(2, 4, weight=10)
    graph_1.add_symetric_link(3, 4, weight=7)
    graph_1.add_symetric_link(4, 5, weight=9)
    print(graph_1)
    print("1 -> 5")
    print(graph_1.dijkstra(1, 5))

    graph_2 = Graph()
    graph_2.add_symetric_link("a", "b", 20)
    graph_2.add_symetric_link("a", "c", 40)
    graph_2.add_symetric_link("a", "d", 10)
    graph_2.add_symetric_link("b", "c", 10)
    graph_2.add_symetric_link("c", "e", 10)
    graph_2.add_symetric_link("d", "e", 10)
    print(graph_2)
    print("a -> e")
    print(graph_2.dijkstra("a", "e"))

    graph_3 = Graph()
    graph_3.add_symetric_link(1, 2, 10)
    graph_3.add_symetric_link(1, 3, 10)
    graph_3.add_symetric_link(1, 10, 200)
    graph_3.add_symetric_link(2, 4, 10)
    graph_3.add_symetric_link(2, 5, 100)
    graph_3.add_symetric_link(2, 7, 10)
    graph_3.add_symetric_link(2, 4, 5)
    graph_3.add_symetric_link(4, 6, 12)
    graph_3.add_symetric_link(6, 7, 20)
    graph_3.add_symetric_link(7, 8, 20)
    graph_3.add_symetric_link(8, 9, 1)
    graph_3.add_symetric_link(8, 11, 10)
    graph_3.add_symetric_link(9, 5, 500)
    graph_3.add_symetric_link(10, 5, 50)
    graph_3.add_symetric_link(11, 5, 10)
    # non-connex for the no-path case
    graph_3.add_symetric_link(500, 501, 10)
    print(graph_3)
    print("1 -> 5")
    print(graph_3.dijkstra(1, 5))

    # test in case there is no path :
    print("1 -> 500 (does not exist)")
    print(graph_3.dijkstra(1, 500))

    # This implementation also works for non-oriented graphs
    non_oriented_graph = Graph()
    non_oriented_graph.add_link(1, 2, 10)
    non_oriented_graph.add_link(1, 5, 5)
    non_oriented_graph.add_link(2, 3, 10)
    non_oriented_graph.add_link(3, 4, 10)
    non_oriented_graph.add_link(1, 4, 60)
    non_oriented_graph.add_link(4, 5, 5)
    print(non_oriented_graph)
    print("1 -> 4")
    print(non_oriented_graph.dijkstra(1, 4))
