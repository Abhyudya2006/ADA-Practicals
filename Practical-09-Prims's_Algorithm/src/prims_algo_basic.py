# prims_matrix_performance.py

import random
import time
import csv

INF = float('inf')

class PrimsMatrix:

    def generate_graph(self, n):
        graph = [[INF]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                w = random.randint(1, 100)
                graph[i][j] = w
                graph[j][i] = w
        return graph

    def prims(self, cost, n):
        near = [0]*n

        min_val = INF
        k = l = 0

        for i in range(n):
            for j in range(n):
                if cost[i][j] < min_val:
                    min_val = cost[i][j]
                    k, l = i, j

        for i in range(n):
            near[i] = k if cost[i][k] < cost[i][l] else l

        near[k] = near[l] = -1

        for _ in range(n-2):
            min_val = INF
            j = -1

            for i in range(n):
                if near[i] != -1 and cost[i][near[i]] < min_val:
                    min_val = cost[i][near[i]]
                    j = i

            near[j] = -1

            for i in range(n):
                if near[i] != -1 and cost[i][near[i]] > cost[i][j]:
                    near[i] = j


def run():
    obj = PrimsMatrix()

    with open("prims_algo_2.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "Time"])

        for n in range(100, 2001, 100):
            g = obj.generate_graph(n)

            start = time.perf_counter()
            obj.prims(g, n)
            end = time.perf_counter()

            writer.writerow([n, end-start])
            print(f"Matrix done for n={n}")

if __name__ == "__main__":
    run()