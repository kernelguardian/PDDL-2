import pydotplus
from graphviz import Graph

# Create a graph object
graph = Graph()

# Add some nodes and edges to the graph
graph.node("A")
graph.node("B")

graph.edge("A", "B")

# Simplify the graph
