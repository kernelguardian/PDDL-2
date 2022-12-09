from pydotplus import graphviz
from pydotplus.graphviz import Graph, Node, Edge
from math import inf


def matrix_to_graph(matrix):
    graph = Graph()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != inf:
                node_i = Node(str(i))
                node_j = Node(str(j))
                graph.add_node(node_i)
                graph.add_node(node_j)
                edge = Edge(node_i, node_j, label=str(matrix[i][j]))
                graph.add_edge(edge)
    return graph


# Example usage
# matrix = [[0, 3, inf, 7], [8, 0, 2, inf], [5, inf, 0, 1], [2, inf, inf, 0]]

# graph = matrix_to_graph(matrix)
# print(graph)
# graph.write_png("graph.png")
