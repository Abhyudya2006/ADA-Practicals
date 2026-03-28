import random
import csv

INF = float('inf')

class Prims:

    def generate_graph(self, n):
        graph = [[INF]*n for _ in range(n)]

        for i in range(n):
            for j in range(i+1, n):
                w = random.randint(1, 20)
                graph[i][j] = w
                graph[j][i] = w

        return graph

    def prims(self, cost, n):
        near = [0]*n
        mst = []
        mincost = 0

        # Find minimum edge
        min_val = INF
        k = l = 0

        for i in range(n):
            for j in range(n):
                if cost[i][j] < min_val:
                    min_val = cost[i][j]
                    k, l = i, j

        mst.append((k, l))
        mincost += cost[k][l]

        # Initialize near[]
        for i in range(n):
            near[i] = k if cost[i][k] < cost[i][l] else l

        near[k] = near[l] = -1

        # Build MST
        for _ in range(n-2):
            min_val = INF
            j = -1

            for i in range(n):
                if near[i] != -1 and cost[i][near[i]] < min_val:
                    min_val = cost[i][near[i]]
                    j = i

            mst.append((j, near[j]))
            mincost += cost[j][near[j]]

            near[j] = -1

            for i in range(n):
                if near[i] != -1 and cost[i][near[i]] > cost[i][j]:
                    near[i] = j

        return mst, mincost


def generate_testcases():
    obj = Prims()

    with open("prims_testcases_with_mst.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "TestCase",
            "Vertices",
            "Adjacency Matrix",
            "MST Edges",
            "Total Cost"
        ])

        for i in range(1, 11):

            n = random.randint(4, 7)
            graph = obj.generate_graph(n)

            mst, cost = obj.prims(graph, n)

            # format matrix
            matrix_str = "; ".join([
                "[" + ", ".join(str(int(x)) if x != INF else "INF" for x in row) + "]"
                for row in graph
            ])

            # format MST
            mst_str = "; ".join([f"({u},{v})" for u, v in mst])

            writer.writerow([i, n, matrix_str, mst_str, cost])

            print(f"Test case {i} done (n = {n})")


if __name__ == "__main__":
    generate_testcases()