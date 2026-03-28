import random
import time
import csv
import heapq

class Kruskal:

    def __init__(self, n):
        self.n = n
        self.parent = [-1]*n

    def find(self, u):
        while self.parent[u] != -1:
            u = self.parent[u]
        return u

    def union(self, u, v):
        self.parent[v] = u

    def kruskal(self, edges):
        heapq.heapify(edges)

        mst_cost = 0
        count = 0

        while count < self.n - 1 and edges:
            w, u, v = heapq.heappop(edges)

            j = self.find(u)
            k = self.find(v)

            if j != k:
                mst_cost += w
                self.union(j, k)
                count += 1

        return mst_cost


# ---------- GRAPH GENERATION ----------

def generate_dense(n):
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            w = random.randint(1, 100)
            edges.append((w, i, j))
    return edges


def generate_sparse(n):
    edges = []

    # ensure connectivity (chain)
    for i in range(n-1):
        w = random.randint(1, 100)
        edges.append((w, i, i+1))

    # few extra edges
    for _ in range(n):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v:
            w = random.randint(1, 100)
            edges.append((w, u, v))

    return edges


# ---------- PERFORMANCE ----------

def run():
    with open("kruskal_sparse_dense.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "Dense_Time", "Sparse_Time"])

        for n in range(100, 5001, 200):

            # Dense
            dense_edges = generate_dense(n)
            obj = Kruskal(n)

            start = time.perf_counter()
            obj.kruskal(dense_edges.copy())
            t_dense = time.perf_counter() - start

            # Sparse
            sparse_edges = generate_sparse(n)
            obj = Kruskal(n)

            start = time.perf_counter()
            obj.kruskal(sparse_edges.copy())
            t_sparse = time.perf_counter() - start

            writer.writerow([n, t_dense, t_sparse])
            print(f"Done for n = {n}")


if __name__ == "__main__":
    run()