import random
import time
import csv
import heapq

class Kruskal:

    def __init__(self, n):
        self.n = n
        self.parent = [-1] * n   # as in pseudocode

    # ---------- FIND ----------
    def find(self, u):
        while self.parent[u] != -1:
            u = self.parent[u]
        return u

    # ---------- UNION ----------
    def union(self, u, v):
        self.parent[v] = u

    # ---------- KRUSKAL ----------
    def kruskal(self, edges):
        heapq.heapify(edges)   # heapify edges

        mst_edges = []
        mincost = 0
        i = 0

        while i < self.n - 1 and edges:
            w, u, v = heapq.heappop(edges)   # delete min edge

            j = self.find(u)
            k = self.find(v)

            if j != k:
                mst_edges.append((u, v, w))
                mincost += w
                self.union(j, k)
                i += 1

        return mst_edges, mincost


# ---------- GRAPH GENERATION ----------
def generate_graph(n): #Generates connected graph
    edges = []

    for i in range(n):
        for j in range(i+1, n):
            w = random.randint(1, 100)
            edges.append((w, i, j))   # heap format (weight first)

    return edges


# ---------- PERFORMANCE ANALYSIS ----------
def performance_analysis():
    with open("kruskal_performance_2.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Vertices", "Edges", "Time_Taken"])

        # 🔥 range of vertices
        for n in range(500, 7001, 500):

            edges = generate_graph(n)

            obj = Kruskal(n)

            start = time.perf_counter()
            obj.kruskal(edges.copy())
            end = time.perf_counter()

            time_taken = end - start
            num_edges = len(edges)

            writer.writerow([n, num_edges, time_taken])
            print(f"Done for n = {n}")


if __name__ == "__main__":
    performance_analysis()