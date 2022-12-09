import pydotplus
import numpy as np
from math import inf
import ast
import csv



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


print("MATRIX_SIZE:", MATRIX_SIZE, " ", len(nodes) + 1)
MATRIX_SIZE = len(nodes) + 1

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
    print(src, dest, value)

    matrix[src][dest] = round(float(value[1]), 2)

# # Fill up first column
# for i in range(len(matrix)):
#     matrix[i][0] = -matrix[0][i]

# # Make diagonal elements zero
# matrix = [
#     [0 if i == j else matrix[i][j] for j in range(len(matrix[i]))]
#     for i in range(len(matrix))
# ]

# create a csv.writer object
with open("matrix.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for row in matrix:
        writer.writerow(row)


from floyd_test import FLOYD_WARSHALL

fw_obj = FLOYD_WARSHALL(G=matrix)
distance = fw_obj.get_distance()

print("Distance\n\n", distance)

from matrix_to_graph import matrix_to_graph

final_graph = matrix_to_graph(distance)
simplified_graph = final_graph.get_simplify()

temp = final_graph.to_string()

with open("finalgraph.dot", "w") as f:
    f.write(temp)

final_graph.set_simplify(True)

temp = final_graph.to_string()

with open("finalgraphSimplify.dot", "w") as f:
    f.write(temp)
