import json
from collections import namedtuple

Edge = namedtuple("Edge", "start, end, weight")


def make_edge(start, end, weight=1):
    return Edge(start, end, weight)


class Graph:
    """A class used to handle graphs, containing shortest route algorithm."""

    def __init__(self, edges):
        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def nodes(self):
        return set(sum(([edge.start, edge.end] for edge in self.edges), []))

    # def get_node_pairs(self, node1, node2, undirected=True):
    #     node_pairs = [[node1, node2]]
    #     if undirected:
    #         node_pairs.append([node2, node1])
    #     return node_pairs
    #
    # def remove_edge(self, node1, node2, undirected=True):
    #     node_pairs = self.get_node_pairs(node1, node2, undirected)
    #     edges = self.edges[:]
    #     for edge in edges:
    #         if [edge.start, edge.end] in node_pairs:
    #             self.edges.remove(edge)
    #
    # def add_edge(self, node1, node2, weight=1, undirected=True):
    #     node_pairs = self.get_node_pairs(node1, node2, undirected)
    #     for edge in self.edges:
    #         if [edge.start, edge.end] in node_pairs:
    #             return ValueError(f"Edge {node1} {node2} already exists")
    #
    #     self.edges.append(Edge(start=node1, end=node2, weight=weight))
    #     if undirected:
    #         self.edges.append(Edge(start=node2, end=node1, weight=weight))

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
        while previous_nodes[current_node]:
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
        Returns an array that contains objects with names of all stops.
    get_stop_id(name)
        Returns a stop id.
    get_stop_name(id)
        Returns a stop name.
    get_shortest_route(source_name, target_name)
        Returns an object that contains shortest route and distance between
        two stops.
    get_all_links()
        Returns an array that contains all links between stops.
    cache_route(route, distance)
        Caches the shortest route between source and target, to reduce the
        amount of unnecessary calculations.
    get_cached_route(source_name, target_name, undirected=True)
        Returns cached shortest route and distance between source and
        target.
    get_all_cached_routes()
        Returns all already cached routes.
    """

    solvro_map = ""

    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            The path to the directory where files with the city map and cashe
            are stored.
        """

        self.path = path
        self.solvro_map = json.load(open(path + "/solvro_city.json", "r"))

    def get_all_stops(self):
        """Returns array that contains objects with names of all stops."""

        output = []
        for node in self.solvro_map["nodes"]:
            # format the output
            output.append({"name": node["stop_name"]})
        return output

    def get_stop_id(self, name):
        """Returns a stop id.

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
            if (
                isinstance(name, str)
                and name.upper() == node["stop_name"].upper()
            ):
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
        """Returns shortest route and distance between two stops.

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

        # check if route hasn't been cached
        cached_route = self.get_cached_route(source_name, target_name)
        if cached_route:
            return cached_route

        # create a graph
        links = []
        for link in self.solvro_map["links"]:
            links.append([link["source"], link["target"], link["distance"]])
        graph = Graph(links)

        # find shortest route
        dijkstra = graph.dijkstra(source_id, target_id)
        if not dijkstra["route"]:
            # if source and target are not connected, return False
            return False

        route = []
        # format the output
        for stop_id in dijkstra["route"]:
            route.append({"name": self.get_stop_name(stop_id)})

        # cache the route
        self.cache_route(route, dijkstra["distance"])

        return {"route": route, "distance": dijkstra["distance"]}

    def get_all_links(self):
        """Returns all links between stops.

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

    def cache_route(self, route, distance):
        """Caches the shortest route between source and target, to reduce the
        amount of unnecessary calculations.

        Parameters
        ----------
        route : array
            An array that contains names of visited stops from the source to
            the target.
        distance : int
            Summary distance of the route.
        """

        routes = self.get_all_cached_routes()
        routes.append({"route": route, "distance": distance})
        open(self.path + "/cache.json", "w").write(json.dumps(routes))

    def get_cached_route(self, source_name, target_name, undirected=True):
        """Returns cached shortest route and distance between source and
        target.

        Parameters
        ----------
        source_name : str
            Name of the source stop.
        target_name : str
            Name of the target stop.
        undirected=True : bool
            Indicates whether order of the source and the target is important.

        Returns
        -------
        object
            If route has been cached, an object that contains shortest route
            and distance between source and target.
        False
            If route hasn't been cached.
        """

        try:
            cached_routes = json.load(open(self.path + "/cache.json", "r"))
            for cached_route in cached_routes:
                if (
                    cached_route["route"][0]["name"] == source_name
                    and cached_route["route"][-1]["name"] == target_name
                ) or (
                    undirected
                    and cached_route["route"][0]["name"] == target_name
                    and cached_route["route"][-1]["name"] == source_name
                ):
                    return cached_route
        except FileNotFoundError:
            return False

        return False

    def get_all_cached_routes(self):
        """Returns all already cached routes.

        Returns
        -------
        array
            An array that contains all cached routes.
        """
        try:
            return json.load(open(self.path + "/cache.json", "r"))
        except FileNotFoundError:
            return []
