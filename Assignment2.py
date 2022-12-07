import math

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


def make_stn(plan):
    #  Part 1 of assignment, parse an STN
    # Complete and then call print function
    # You should return nodes and edges in 2 lists

    print_stn(nodes, edges, graph)

    return nodes, edges, graph


def print_stn(nodes, edges, graph):
    # Part 2, print the STN
    # Complete this

    print("digraph {")


def floyd_warshall(nodes, edges, graph):
    # Part 3, floyd warshall
    # Complete and return a boolean value

    return True, nodes, edges, graph


def make_minimal(nodes, edges, graph):
    # Make minimal graph
    # Return nodes and edges
    return nodes, edges, graph
