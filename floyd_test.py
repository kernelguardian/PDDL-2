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

        self.print_solution(distance)
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
