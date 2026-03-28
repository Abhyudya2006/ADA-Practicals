import random
import csv

INF = float('inf')

class Dijkstra:

    def generate_graph(self, n):
        cost = [[INF for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.6:
                    cost[i][j] = random.randint(1, 20)

        return cost

    def dijkstra_algo(self, cost, v, n):
        S = [False]*n
        dist = [INF]*n
        visit_order = []

        for i in range(n):
            dist[i] = cost[v][i]

        S[v] = True
        dist[v] = 0
        visit_order.append(v)

        for _ in range(1, n):
            min_val = INF
            u = -1

            for i in range(n):
                if not S[i] and dist[i] < min_val:
                    min_val = dist[i]
                    u = i

            if u == -1:
                break

            S[u] = True
            visit_order.append(u)

            for w in range(n):
                if not S[w] and cost[u][w] != INF:
                    if dist[w] > dist[u] + cost[u][w]:
                        dist[w] = dist[u] + cost[u][w]

        return tuple(visit_order), dist


def generate_examples():
    obj = Dijkstra()

    with open("dijkstra_final_eg.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "TestCase",
            "Vertices",
            "Cost_Matrix",
            "Visit_Order",
            "Min_Cost"
        ])

        for i in range(1, 11):

            n = random.randint(4, 8)
            graph = obj.generate_graph(n)

            order, dist = obj.dijkstra_algo(graph, 0, n)

            # Convert matrix to string (simple readable form)
            matrix_str = "; ".join([
                ",".join(str(int(x)) if x != INF else "INF" for x in row)
                for row in graph
            ])

            writer.writerow([
                i,
                n,
                matrix_str,
                order,
                dist
            ])

            print(f"Example {i} done (n = {n})")


if __name__ == "__main__":
    generate_examples()