import math
import re
import pydotplus
import pprint
import csv
import pydot
import numpy as np
import networkx as nx

pp = pprint.PrettyPrinter(indent=4, width=41, compact=True)

input_lines_list = []
nodes = []
edges = []
start_times = []
time_dict = []


graph = None

# Update, as some of you are doing separate nodes and edges,
# and others are using the graph directly, then I will provide
# you the option.  You can use lists of nodes and edges, or you
# can use/make the graph directly.

# I will check all three so you do not need to do both approaches.
# Either pass in and return lists of edges and nodes and set graph
# to none (and don't use it), or use graph and keep nodes and edges
# empty.


def make_stn(plan):
    #  Part 1 of assignment, parse an STN
    # Complete and then call print function
    # You should return nodes and edges in 2 lists

    with open("test_dot.dot", "w") as output_header:
        output_header.write("digraph plan {\n")
        with open(plan, "r") as plan_lines:
            for lines in plan_lines:
                input_lines_list.append(lines)
            # input_lines_list.reverse()
        line_count = len(input_lines_list)
        for line in input_lines_list:
            match_node = re.search("\\(([^)]+)\\)", line)
            if match_node:
                nodes.append(match_node.group(1))
            start_time = line.split(":")[0]
            end_match = re.search("\\[([^)]+)\\]", line)
            end_time = None
            if end_match:
                end_time = end_match.group(1)
                list = [float(start_time), float(end_time)]
                edges.append(list)

    # print(nodes)
    # print(edges)
    print_stn(nodes, edges, graph=None)
    global graph
    graph = pydotplus.graphviz.graph_from_dot_file("test_dot_final.dot")
    return nodes, edges, graph


def print_stn(nodes, edges, graph):
    # Part 2, print the STN
    # Complete this
    step_lengeth = len(nodes)
    nodes.reverse()
    with open("test_dot_final.dot", "w") as output_header:
        output_header.write("digraph plan {\n")
        for node in nodes:
            output_header.write(
                "Step"
                + str(step_lengeth)
                + ' [label="Step '
                + str(step_lengeth)
                + ": ("
                + node
                + ')"];\n'
            )
            step_lengeth -= 1
        output_header.write('Z [label="Z"];\n')
        edge_length = 1
        output_header.write('Z -> Z [label="[0,0]"];\n')
        for edge in edges:
            output_header.write(
                "Z -> Step" + str(edge_length) + '[label="[0,' + str(edge[0]) + ']"];\n'
            )
            edge_length += 1
        edge_length = 1
        step_lengeth = len(nodes)
        for edge in edges:
            if edge_length <= step_lengeth:
                output_header.write(
                    "Step"
                    + str(edge_length)
                    + " -> "
                    + "Step"
                    + str(edge_length + 1)
                    + '[label="['
                    + str(edge[1])
                    + ","
                    + str(edge[1])
                    + ']"];\n'
                )
                edge_length += 1
        output_header.write("}\n")
        # print(dot)


def floyd_warshall(nodes, edges, graph):
    # Part 3, floyd warshall
    # Complete and return a boolean value
    # print(edges)
    edg = graph.get_edge_list()
    nods = graph.get_node_list()
    # print(len(nods))
    matrix = [[0.0 for _ in range(len(nods))] for _ in range(len(nods))]
    nods.reverse()
    for i in range(len(nods) - 1):
        for j in range(len(nods) - 1):
            if i == j:
                matrix[i][j] = 0
            else:
                matrix[i][j] = 9999.99
            j += 1
        i += 1
    # print(matrix)
    # for i in edg:
    #     print(i.obj_dict['attributes']['label'])
    # for i in nods:
    #     print(i.get_name())
    for i in range(len(nods)):
        j = edg[i]
        source = j.obj_dict["attributes"]["label"]
        split = source.split(",")[1].split("]")[0]
        if i != 0:
            matrix[0][i] = float(split)
            matrix[i][0] = -float(split)
    # pp.pprint(matrix)
    # with open("mat.csv",'w', newline="") as csvfile:
    #     writer = csv.writer(csvfile)
    #     for row in matrix:
    #         writer.writerow(row)
    # for i in range(len(nods)):
    #     matrix[i][i+1] = edge
    new_edges = []
    for ed in edg:
        source = ed.obj_dict["attributes"]["label"]
        split = source.split(",")[0].split("[")[1]
        if split != "0":
            new_edges.append(split)
    # print(new_edges)

    for i in range(len(new_edges)):
        matrix[i][i + 1] = float(new_edges[i])
        matrix[i + 1][i] = -float(new_edges[i])

    # with open("mat.csv",'w', newline="") as csvfile:
    #     writer = csv.writer(csvfile)
    #     for row in matrix:
    #         writer.writerow(row)
    inf = math.inf
    # matrix = [[0, 6, 4, inf, inf],
    #      [-3, 0, inf, 6, inf],
    #      [0, inf, 0, inf, 5],
    #      [inf, -3, inf, 0, 6],
    #      [inf, inf, 0, -3, 0]]
    n = len(matrix)
    for i in range(n):
        # print(i)
        if matrix[i][i] < 0:
            print("Inconsistant")
            return False
        else:
            for k in range(n):
                for i in range(n):
                    for j in range(n):
                        matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])
            with open("mat_floyd.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                for row in matrix:
                    writer.writerow(row)
            # pp.pprint(distance)
            matrix = np.array(matrix)
            nxgraph = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph)
            graph = nx.nx_pydot.to_pydot(nxgraph)
            make_minimal(nodes, edges, graph)
            return True, nodes, edges, graph


def printSolution(dist, V):
    print(
        "Following matrix shows the shortest distances\
 between every pair of vertices"
    )
    for i in range(V):
        for j in range(V):
            if dist[i][j] == math.inf:
                print("%7s" % ("INF"), end=" ")
            else:
                print("%7d\t" % (dist[i][j]), end=" ")
            if j == V - 1:
                print()


def make_minimal(nodes, edges, graph):
    # Make minimal graph
    # Return nodes and edges
    nodes = graph.get_node_list()
    edges = graph.get_edge_list()

    graph_dict = {}

    for n1 in nodes:
        node_details_dict = {}
        for e in edges:

            # print(n1)
            # print(e.get_source())

            if e.get_source() == (n1.get_name()):
                # print("Matched")

                edge_value = float(e.obj_dict["attributes"]["weight"])
                dest = e.get_destination()
                # print(dest)
                # print(edge_value)
                node_details_dict[dest] = edge_value

        graph_dict[n1.get_name()] = node_details_dict

    for n in nodes:
        for n1 in nodes:
            for n2 in nodes:
                x = n.get_name()
                x1 = n1.get_name()
                x2 = n2.get_name()
                if (x != '"\\n"') and (x1 != '"\\n"') and (x2 != '"\\n"'):
                    if (x1 != x2) and (x1 != x) and (x2 != x):
                        try:
                            if abs(graph_dict[x1][x2]) == (
                                abs(graph_dict[x1][x]) + abs(graph_dict[x][x2])
                            ):
                                if (graph_dict[x][x2] >= 0) and (
                                    graph_dict[x1][x2] >= 0
                                ):
                                    graph_dict[x1].pop(x2)
                                if (graph_dict[x1][x] < 0) and (graph_dict[x1][x2] < 0):
                                    graph_dict[x1].pop(x2)
                        except KeyError as e:
                            #                  print(str("The node "+str(e)+" is disconnected"))
                            pass

    min_graph = pydot.Dot("min_graph", graph_type="digraph", bgcolor="white")

    for dict_node in graph_dict:
        min_graph.add_node(pydot.Node(dict_node, shape="circle"))

    for dict_key, dict_value in graph_dict.items():
        for dict_value_key, dict_value_value in dict_value.items():
            min_graph.add_edge(
                pydot.Edge(
                    dict_key, dict_value_key, color="blue", label=dict_value_value
                )
            )

    graph.write_raw("output_raw.dot")
    return nodes, edges, min_graph


# Functiion is called from this part
make_stn("temporalplan.pddl")
value = floyd_warshall(nodes, edges, graph)
if value:
    print("Graph Consistant")
else:
    print("Inconsistant")
