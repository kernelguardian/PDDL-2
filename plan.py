from typing import List, Tuple
import pprint

pp = pprint.PrettyPrinter(width=41, compact=True)


def load_file(filename: str):
    with open(filename, "r") as fhandler:
        file_contents = fhandler.read().split("\n")
        nodes = [_[_.find("(") : _.rfind(")") + 1] for _ in file_contents]
        # print("==========Nodes==========\n{}".format(nodes))

        edges = [_[_.find("[") + 1 : _.rfind("]")] for _ in file_contents]
        # print("==========Edges==========\n{}".format(edges))

        timevalues = [_[: _.rfind(":")] for _ in file_contents]
        # print("==========TimeValues==========\n{}".format(timevalues))
        pp.pprint(timevalues)
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


nodes, edges, timevalues = load_file(
    "/Users/fluffyunicorn/Desktop/Uni/Semester 1/Reasoning Assignment 2/temporalplan.pddl"
)


write_dot(nodes=nodes, edges=edges, timevalues=timevalues)
