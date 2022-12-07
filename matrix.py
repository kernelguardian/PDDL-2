import pprint
import numpy as np
from floyd_test import floyd_warshall

nV = 103
pp = pprint.PrettyPrinter(width=41, compact=True)


def matrix_parser(filename="output.dot"):
    with open(filename, "r") as fhandler:
        dot_file = fhandler.read().splitlines()
        # pp.pprint(dot_file)

    values = []

    for line in dot_file:
        if str.find(line, "->") != -1:
            a = line.split("->")[0].replace(" ", "")
            b = line.split("->")[1].split("[")[0].replace(" ", "")
            c = (
                line.split("=")[1]
                .replace('"', "")
                .replace("]", "")
                .replace(";", "")
                .replace(" ", "")
            )
            values.append([a, b, c])
    return values


values = matrix_parser(filename="output.dot")
array = np.full((nV, nV), np.inf)

for value in values:

    if value[0] == "Z" or value[1] == "Z":
        pass
    else:
        row = int(value[0].replace("Step", ""))

        column = int(value[1].replace("Step", ""))
        edge_value = value[2]

        array[row][column] = edge_value

print(array)
np.savetxt("foo.csv", array, delimiter=",")
floyd_warshall(array)
# print(values)
