from pydotplus import graphviz
from pydotplus.graphviz import Graph, Node, Edge
import networkx as nx


def minimal_spanning_tree(graph):
    # Create a Graph object from the original graph
    G = Graph()
    for edge in graph.edges:
        node1 = Node(edge[0])
        node2 = Node(edge[1])
        weight = graph[edge[0]][edge[1]]["weight"]
        G.add_node(node1)
        G.add_node(node2)
        G.add_edge(Edge(node1, node2, label=str(weight)))

    # Compute the minimum spanning tree using Kruskal's algorithm
    T = nx.minimum_spanning_tree(G)

    # Create a Graph object from the minimum spanning tree
    T_graph = Graph()
    for edge in T.edges(data=True):
        node1 = Node(edge[0])
        node2 = Node(edge[1])
        weight = edge[2]["weight"]
        T_graph.add_node(node1)
        T_graph.add_node(node2)
        T_graph.add_edge(Edge(node1, node2, label=str(weight)))

    return T_graph


# Example usage
graph = {
    "A": {"B": {"weight": 2}, "C": {"weight": 3}},
    "B": {"A": {"weight": 2}, "C": {"weight": 1}, "D": {"weight": 4}},
    "C": {"A": {"weight": 3}, "B": {"weight": 1}, "D": {"weight": 5}},
    "D": {"B": {"weight": 4}, "C": {"weight": 5}},
}

minimal_graph = minimal_spanning_tree(graph)
minimal_graph.write_png("minimal_graph.png")
