import json
from collections import namedtuple

Edge = namedtuple("Edge", "start, end, weight")


def make_edge(start, end, weight=1):
    return Edge(start, end, weight)


class PK_Graph:
    """A class used to handle graphs, containing shortest route algorithm."""

    def __init__(self, edges):
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError(f"Wrong edges detected: {wrong_edges}")

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def nodes(self):
        return set(sum(([edge.start, edge.end] for edge in self.edges), []))

    def get_node_pairs(self, node1, node2, both_ends=True):
        node_pairs = [[node1, node2]]
        if both_ends:
            node_pairs.append([node2, node1])
        return node_pairs

    def remove_edge(self, node1, node2, both_ends=True):
        node_pairs = self.get_node_pairs(node1, node2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, node1, node2, weight=1, both_ends=True):
        node_pairs = self.get_node_pairs(node1, node2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError(f"Edge {node1} {node2} already exists")

        self.edges.append(Edge(start=node1, end=node2, weight=weight))
        if both_ends:
            self.edges.append(Edge(start=node2, end=node1, weight=weight))

    @property
    def neighbours(self):
        neighbours = {node: set() for node in self.nodes}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.weight))
        return neighbours

    def dijkstra(self, source, target):
        assert source in self.nodes, "Such source node deos not exist"

        if source == target:
            return {"route": [source], "distance": 0}

        distances = {node: float("inf") for node in self.nodes}
        previous_nodes = {node: None for node in self.nodes}
        distances[source] = 0
        nodes = self.nodes.copy()

        while nodes:
            current_node = min(nodes, key=lambda node: distances[node])
            nodes.remove(current_node)
            if distances[current_node] == float("inf"):
                break
            for neighbour, weight in self.neighbours[current_node]:
                alternative_route = distances[current_node] + weight
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_nodes[neighbour] = current_node

        current_node, route = target, []
        while previous_nodes[current_node] is not None:
            route.insert(0, current_node)
            current_node = previous_nodes[current_node]
        if route:
            route.insert(0, current_node)
        return {"route": route, "distance": distances[target]}


class SolvroCity:
    """
    A class that allows us to get information about Solvro City stops.

    ...

    Attributes
    ----------
    solvro_map : object
        An object that contains a raw Solvro City map.

    Methods
    -------
    get_all_stops()
        Returns array that contains objects with names of all stops.
    get_stop_id(name)
        Returns stop id.
    get_stop_name(id)
        Returns stop name.
    get_shortest_route(source_name, target_name)
        Returns object that contains shortest route and distance between
        two stops.
    get_all_links()
        Returns array that contains all links between stops.
    """

    solvro_map = ""

    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            The path to the JSON file with a city map.
        """

        self.solvro_map = json.load(open(path, "r"))

    def get_all_stops(self):
        """Returns array that contains objects with names of all stops."""

        output = []
        for node in self.solvro_map["nodes"]:
            # format the output
            output.append({"name": node["stop_name"]})
        return output

    def get_stop_id(self, name):
        """Returns stop id.

        Parameters
        ----------
        name : str
            A name of the stop.

        Returns
        -------
        node["id"] : int
            An id of the stop.

        Raises
        ------
        ValueError
            If stop with provided name doesn't exist.
        """

        for node in self.solvro_map["nodes"]:
            if isinstance(name, str) and name.upper() == node["stop_name"].upper():
                return node["id"]
        raise ValueError("stop not found")

    def get_stop_name(self, id):
        """Returns stop name.

        Parameters
        ----------
        id : int
            An id of the stop.

        Returns
        -------
        node["stop_name"] : str
            A name of the stop.

        Raises
        ------
        ValueError
            If stop with provided id doesn't exist.
        """

        for node in self.solvro_map["nodes"]:
            if id == node["id"]:
                return node["stop_name"]
        raise ValueError("stop not found")

    def get_shortest_route(self, source_name, target_name):
        """Returns object that contains shortest route and distance between
        two stops.

        Parameters
        ----------
        source_name : str
            A name of the source node.
        target_name : str
            A name of the target node.

        Returns
        -------
        object
            If sourca node and target node are connected, an object that
            contains shortest route and distance between them.
        False
            If source node and target node are not connected.

        Raises
        ------
        ValueError
            If source node or target node with provided name doesn't exist.
        """

        # check if source exists
        source_id = self.get_stop_id(source_name)
        if source_id is False:
            raise ValueError("source not found")

        # check if target exists
        target_id = self.get_stop_id(target_name)
        if target_id is False:
            raise ValueError("target not found")

        # create a graph
        links = []
        for link in self.solvro_map["links"]:
            links.append([link["source"], link["target"], link["distance"]])
        graph = PK_Graph(links)

        # find shortest route
        dijkstra = graph.dijkstra(source_id, target_id)
        if not dijkstra["route"]:
            # if it is impossible to get from source to destination, return False
            return False

        stops = []
        # format the output
        for stop_id in dijkstra["route"]:
            stops.append({"name": self.get_stop_name(stop_id)})

        return {"stops": stops, "distance": dijkstra["distance"]}

    # returns all links
    def get_all_links(self):
        """Returns array that contains all links between stops.

        Returns
        -------
        output : array
            An array that contains objects with links data.
        """

        output = []
        for link in self.solvro_map["links"]:
            # format the output
            output.append(
                {
                    "source": self.get_stop_name(link["source"]),
                    "target": self.get_stop_name(link["target"]),
                    "distance": link["distance"],
                }
            )
        return output
