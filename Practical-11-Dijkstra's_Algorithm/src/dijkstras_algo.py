import random
import time
import csv

INF = float('inf')

class dijkstra:

    def generate_graph(self, n):
        cost = [[INF for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.6:
                    cost[i][j] = random.randint(1, 50)

        return cost
    
    def dijkstra_algo(self, cost, v, n):
        S = [False]*n
        dist = [INF]*n

        for i in range(n):
            dist[i] = cost[v][i]

        S[v] = True
        dist[v] = 0

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

            for w in range(n):
                if not S[w] and cost[u][w] != INF:
                    if dist[w] > dist[u] + cost[u][w]:
                        dist[w] = dist[u] + cost[u][w]

        return dist


def performance_analysis():
    obj = dijkstra()

    with open("dijkstra_performance_2.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['Vertices', 'Time_taken'])

        for n in range(500, 5001, 250):
            graph = obj.generate_graph(n)   

            start = time.perf_counter()
            obj.dijkstra_algo(graph, 0, n)
            end = time.perf_counter()

            writer.writerow([n, end - start])
            print(f'Done for n={n}')


if __name__ == "__main__":
    performance_analysis()