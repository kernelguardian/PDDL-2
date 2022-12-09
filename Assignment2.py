import pydotplus
import numpy as np
from math import inf
import ast
import csv
import pprint
from pydotplus import graphviz
from pydotplus.graphviz import Graph, Node, Edge


pp = pprint.PrettyPrinter(width=41, compact=True)


nodes = []
edges = []

graph = None

# Update, as some of you are doing separate nodes and edges,
# and others are using the graph directly, then I will provide
# you the option.  You can use lists of nodes and edges, or you
# can use/make the graph directly.

# I will check all three so you do not need to do both approaches.
# Either pass in and return lists of edges and nodes and set graph
# to none (and don't use it), or use graph and keep nodes and edges
# empty.

distance = []


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


class FLOYD_WARSHALL:
    def __init__(self, G, nV=102) -> None:

        self.nV = nV
        self.INF = float("inf")
        self.distance = self.floyd_warshall(G=G)

    def floyd_warshall(self, G):
        distance = list(map(lambda i: list(map(lambda j: j, i)), G))

        # Adding vertices individually
        for i in range(self.nV):
            if distance[i][i] < 0:
                return False
            else:
                for k in range(self.nV):
                    for i in range(self.nV):
                        for j in range(self.nV):
                            distance[i][j] = min(
                                distance[i][j], distance[i][k] + distance[k][j]
                            )

        # self.print_solution(distance)
        # print("\nhm", distance)
        return distance

    # Printing the solution
    def print_solution(self, distance):
        for i in range(self.nV):
            for j in range(self.nV):
                if distance[i][j] == self.INF:
                    print("INF", end=" ")
                else:
                    print(distance[i][j], end="  ")
            print(" ")

    def get_distance(self):
        return self.distance


def load_file(filename: str):
    with open(filename, "r") as fhandler:
        file_contents = fhandler.read().split("\n")
        nodes = [_[_.find("(") : _.rfind(")") + 1] for _ in file_contents]
        # print("==========Nodes==========\n{}".format(nodes))

        edges = [_[_.find("[") + 1 : _.rfind("]")] for _ in file_contents]
        # print("==========Edges==========\n{}".format(edges))

        timevalues = [_[: _.rfind(":")] for _ in file_contents]
        # print("==========TimeValues==========\n{}".format(timevalues))
        # pp.pprint(timevalues)
        return nodes, edges, timevalues


def write_dot(nodes, edges, timevalues, filename="output.dot"):

    with open(filename, "w") as fout_handler:
        fout_handler.write("digraph plan {\n")

        # Labels
        for i in range(len(nodes)):
            fout_handler.write('Step{} [label="Step{}: {}"]\n'.format(i, i, nodes[i]))

        # Edges Z
        for i in range(len(nodes)):
            fout_handler.write(
                '\tStep{} -> Z [ label="{}" ] \n'.format(
                    i, float(timevalues[-1]) - float(timevalues[i])
                )
            )

        # Edges rest
        for i in range(len(nodes)):
            fout_handler.write(
                '\tStep{} -> Step{} [ label="{}" ] \n'.format(i, i + 1, edges[i])
            )

        fout_handler.write("}")


def make_stn(plan):
    #  Part 1 of assignment, parse an STN
    # Complete and then call print function
    # You should return nodes and edges in 2 lists
    nodes, edges, timevalues = load_file(plan)
    write_dot(nodes=nodes, edges=edges, timevalues=timevalues)

    # print_stn(nodes, edges, graph)

    return nodes, edges, graph


def print_stn(nodes, edges, graph):
    # Part 2, print the STN
    # Complete this
    print("digraph {")


def floyd_warshall(nodes, edges, graph):
    # Part 3, floyd warshall
    # Complete and return a boolean value
    global distance
    with open("output.dot", "r") as f:
        raw_dot = f.read()

    dot = pydotplus.graphviz.graph_from_dot_file("output.dot")
    edges = dot.get_edge_list()
    nodes = dot.get_node_list()

    # Gimmick code
    MATRIX_SIZE = (
        int(
            raw_dot[raw_dot.find("{\nStep") + 2 : raw_dot.find("[label")].removeprefix(
                "Step"
            )
        )
        + 2
    )

    matrix = [[inf for i in range(MATRIX_SIZE)] for j in range(MATRIX_SIZE)]

    for edge in edges:
        src = edge.get_source()
        dest = edge.get_destination()
        value = ast.literal_eval(edge.get("label").replace('"', ""))

        # print(src, dest, value)

        if src == "Z":
            src = 0
        else:
            src = int(src.replace("Step", ""))

        dest = int(dest.replace("Step", ""))
        # print(src, dest, value)

        matrix[src][dest] = round(float(value[1]), 2)

    # Uncomment this
    # Fill up first column
    for i in range(len(matrix)):
        matrix[i][0] = -matrix[0][i]

    # Make diagonal elements zero
    matrix = [
        [0 if i == j else matrix[i][j] for j in range(len(matrix[i]))]
        for i in range(len(matrix))
    ]

    with open("matrix.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in matrix:
            writer.writerow(row)

    fw_obj = FLOYD_WARSHALL(G=matrix)

    distance = fw_obj.get_distance()
    if distance is False:
        print("inconsistent")
        return False
    else:
        return True
    # return distance


def make_minimal(nodes, edges, graph):
    # Make minimal graph
    # Return nodes and edges
    final_graph = matrix_to_graph(distance)
    temp = final_graph.to_string()

    with open("finalgraph.dot", "w") as f:
        f.write(temp)

    # Todo simplify here
    return nodes, edges, graph


nodes, edges, graph = make_stn(
    "/Users/fluffyunicorn/Desktop/Uni/Semester 1/Reasoning Assignment 2/temporalplan.pddl"
)

print_stn(nodes, edges, graph)

floyd_warshall(nodes, edges, graph)
make_minimal(nodes, edges, graph)
