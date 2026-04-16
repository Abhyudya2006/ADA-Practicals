import math

def f_graph_matrix_version():
    print("--- Multistage Graph Shortest Path (FGraph) ---")
    
    # 1. Structural Inputs
    k = int(input("Enter the number of stages (k): "))
    n = int(input("Enter the total number of vertices (n): "))
    
    # 2. Stage Distribution
    print("\n--- Stage Distribution ---")
    stage_map = {}
    for i in range(1, k + 1):
        v_list = input(f"Enter vertex IDs in Stage {i} (space-separated): ")
        stage_map[i] = [int(v) for v in v_list.split()]

    # 3. Full Matrix Input
    print(f"\n--- Cost Matrix ({n}x{n}) ---")
    print(f"Enter the costs row by row. Use 'inf' for no connection.")
    print(f"Example for 3 vertices: \n0 5 10\ninf 0 3\ninf inf 0")
    
    # Initialize n+1 matrix to match 1-based indexing in pseudocode
    matrix = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        row_input = input(f"Row {i} (costs to vertices 1 to {n}): ").split()
        for j, val in enumerate(row_input):
            dest_vertex = j + 1
            if val.lower() != 'inf':
                matrix[i][dest_vertex] = float(val)

    # 4. Algorithm Setup
    cost = [0.0] * (n + 1)
    d = [0] * (n + 1)
    p = [0] * (k + 1)
    
    # Line 6: cost[n] := 0.0
    cost[n] = 0.0
    
    print("\n--- Start of Iterations (Backward Pass) ---")
    
    # 5. Backward Iteration (Lines 7 - 13)
    for j in range(n - 1, 0, -1):
        print(f"\nComputing for Vertex {j}:")
        min_cost = float('inf')
        best_r = -1
        
        # We look for vertex 'r' such that <j, r> is an edge
        for r in range(j + 1, n + 1):
            edge_weight = matrix[j][r]
            if edge_weight != float('inf'):
                current_total = edge_weight + cost[r]
                print(f"  -> Path through {r}: edge_weight({edge_weight}) + cost[{r}]({cost[r]}) = {current_total}")
                
                if current_total < min_cost:
                    min_cost = current_total
                    best_r = r
        
        cost[j] = min_cost
        d[j] = best_r
        print(f"  ** Updation: cost[{j}] = {cost[j]}, d[{j}] = {d[j]} **")

    # 6. Find Minimum Cost Path (Lines 15 - 16)
    print("\n--- Path Reconstruction ---")
    p[1] = 1
    p[k] = n
    print(f"Setting p[1] = 1, p[{k}] = {n}")
    
    for j in range(2, k):
        p[j] = d[p[j-1]]
        print(f"At Stage {j}: p[{j}] = d[p[{j-1}]] = d[{p[j-1]}] = {p[j]}")

    # Final Output
    path_result = " -> ".join(map(str, [p[i] for i in range(1, k + 1)]))
    print("\n" + "="*40)
    print(f"Final Minimum Cost: {cost[1]}")
    print(f"Final Path: {path_result}")
    print("="*40)

if __name__ == "__main__":
    f_graph_matrix_version()