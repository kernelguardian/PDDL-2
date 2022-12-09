def floyd_warshall(adj_matrix):
    # Get the number of nodes in the graph
    n = len(adj_matrix)

    # Initialize the distances matrix with the adjacency matrix
    distances = adj_matrix.copy()

    # Iterate through the intermediate nodes
    for k in range(n):
        # Iterate through the source nodes
        for i in range(n):
            # Iterate through the destination nodes
            for j in range(n):
                # Check if the distance through the intermediate node
                # is shorter than the current distance
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    # Update the distance with the shorter value
                    distances[i][j] = distances[i][k] + distances[k][j]

    # Check for consistency in the distances matrix
    for i in range(n):
        for j in range(n):
            if distances[i][j] != distances[j][i]:
                # The distances matrix is not consistent
                raise ValueError("Inconsistent distances")

    # Return the distances matrix
    return distances
