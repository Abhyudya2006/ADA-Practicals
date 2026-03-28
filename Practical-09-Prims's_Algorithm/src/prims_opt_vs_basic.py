import random
import time
import csv
import heapq

INF = float('inf')

class PrimsComparison:

    # ---------- GRAPH GENERATION ----------

    def generate_dense_matrix(self, n):
        graph = [[INF]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                w = random.randint(1, 100)
                graph[i][j] = w
                graph[j][i] = w
        return graph

    def generate_sparse_list(self, n):
        graph = {i: [] for i in range(n)}

        # ensure connectivity
        for i in range(n-1):
            w = random.randint(1, 100)
            graph[i].append((i+1, w))
            graph[i+1].append((i, w))

        # few extra edges
        for _ in range(n):
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            if u != v:
                w = random.randint(1, 100)
                graph[u].append((v, w))
                graph[v].append((u, w))

        return graph

    # ---------- CONVERSIONS ----------

    def matrix_to_list(self, mat, n):
        graph = {i: [] for i in range(n)}
        for i in range(n):
            for j in range(n):
                if i != j and mat[i][j] != INF:
                    graph[i].append((j, mat[i][j]))
        return graph

    def list_to_matrix(self, graph, n):
        mat = [[INF]*n for _ in range(n)]
        for u in graph:
            for v, w in graph[u]:
                mat[u][v] = w
        return mat

    # ---------- MATRIX PRIM'S ----------

    def prims_matrix(self, cost, n):
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

    # ---------- HEAP PRIM'S ----------

    def prims_heap(self, graph, n):
        visited = [False]*n
        pq = [(0, 0)]

        while pq:
            w, u = heapq.heappop(pq)

            if visited[u]:
                continue

            visited[u] = True

            for v, wt in graph[u]:
                if not visited[v]:
                    heapq.heappush(pq, (wt, v))


# ---------- PERFORMANCE ----------

def run():
    obj = PrimsComparison()

    with open("prims_full_comparison.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "n",
            "Matrix_Dense",
            "Matrix_Sparse",
            "Heap_Dense",
            "Heap_Sparse"
        ])

        for n in range(100, 2001, 100):

            # Dense
            dense_matrix = obj.generate_dense_matrix(n)
            dense_list = obj.matrix_to_list(dense_matrix, n)

            # Sparse
            sparse_list = obj.generate_sparse_list(n)
            sparse_matrix = obj.list_to_matrix(sparse_list, n)

            # Matrix Dense
            start = time.perf_counter()
            obj.prims_matrix(dense_matrix, n)
            t_md = time.perf_counter() - start

            # Matrix Sparse
            start = time.perf_counter()
            obj.prims_matrix(sparse_matrix, n)
            t_ms = time.perf_counter() - start

            # Heap Dense
            start = time.perf_counter()
            obj.prims_heap(dense_list, n)
            t_hd = time.perf_counter() - start

            # Heap Sparse
            start = time.perf_counter()
            obj.prims_heap(sparse_list, n)
            t_hs = time.perf_counter() - start

            writer.writerow([n, t_md, t_ms, t_hd, t_hs])
            print(f"Done for n = {n}")


if __name__ == "__main__":
    run()