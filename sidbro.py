import math
import re
import pydotplus


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
    graph = print_stn(nodes, edges, graph=None)
    # print(graph)
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
        edge_length = 1
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
        dot = pydotplus.graphviz.graph_from_dot_file("test_dot_final.dot")
        print(dot)


def floyd_warshall(nodes, edges, graph):
    # Part 3, floyd warshall
    # Complete and return a boolean value

    return True, nodes, edges, graph


def make_minimal(nodes, edges, graph):
    # Make minimal graph
    # Return nodes and edges
    return nodes, edges, graph


make_stn("temporalplan.pddl")
