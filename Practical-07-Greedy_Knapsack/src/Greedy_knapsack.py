import random
import time
import pandas as pd

def greedy_knapsack(wts, prof, capacity):
    n = len(wts)
    
    # Calculate profit/weight ratios
    ratio = []
    for i in range(n):
        ratio.append((i, prof[i] / wts[i]))
    
    # Sort by ratio descending: O(n log n)
    ratio.sort(key=lambda x: x[1], reverse=True)
    
    total_profit = 0
    solution = [0] * n
    
    for i, _ in ratio:
        if capacity >= wts[i]:
            solution[i] = 1
            total_profit += prof[i]
            capacity -= wts[i]
        else:
            # Fractional part
            solution[i] = capacity / wts[i]
            total_profit += prof[i] * (capacity / wts[i])
            break
    
    return solution, total_profit

def generate_knapsack_data(n):
    wts = [random.randint(1, 50) for _ in range(n)]
    prof = [random.randint(10, 200) for _ in range(n)]
    capacity_percentage = random.uniform(0.4, 0.6)
    capacity = int(sum(wts) * capacity_percentage)
    
    return wts, prof, capacity

# Loop parameters
start_size = 10000
end_size = 200000
step_size = 10000
trials = 20

sizes = []
avg_times = []

print("Starting Greedy Knapsack Benchmark (Dynamic Capacity: 40-60%)...\n")

overall_start = time.perf_counter()

for n in range(start_size, end_size + 1, step_size):
    print(f"\nTesting n = {n}")
    total_time = 0
    
    for t in range(1, trials + 1):
        wts, prof, capacity = generate_knapsack_data(n)
        
        start = time.perf_counter()
        greedy_knapsack(wts, prof, capacity)
        end = time.perf_counter()
        
        trial_time = (end - start) * 1000  
        total_time += trial_time
        
        if t % 5 == 0: 
            print(f"  Progress: Trial {t:02d} complete")
    
    average_time = total_time / trials
    print(f"  ➤ Average Time for n={n}: {average_time:.4f} ms")
    
    sizes.append(n)
    avg_times.append(average_time)

overall_end = time.perf_counter()

print("\nBenchmark Completed.")
print(f"Total Experiment Time: {overall_end - overall_start:.2f} seconds")

# Save to file using keys that match your plotting script
df = pd.DataFrame({
    "Size": sizes,
    "Avg_Time_ms": avg_times
})

df.to_csv("greedy_knapsack_runtime.csv", index=False)
print("\nFile 'greedy_knapsack_runtime.csv' saved successfully.")