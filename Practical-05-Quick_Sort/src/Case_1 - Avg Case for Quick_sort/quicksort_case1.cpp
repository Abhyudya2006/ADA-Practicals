#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <fstream>
#include <iomanip>
#include <cmath>

using namespace std;
using namespace std::chrono;

/* ================= QUICK SORT ================= */

// Partition using FIRST element as pivot
int partition_first(vector<int>& arr, int low, int high) {
    int pivot = arr[low];
    int i = low + 1;
    int j = high;

    while (true) {
        while (i <= high && arr[i] <= pivot) i++;
        while (j >= low + 1 && arr[j] > pivot) j--;

        if (i >= j) break;
        swap(arr[i], arr[j]);
    }

    swap(arr[low], arr[j]);
    return j;
}

void quick_sort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int p = partition_first(arr, low, high);
        quick_sort(arr, low, p - 1);
        quick_sort(arr, p + 1, high);
    }
}

/* ================= MAIN EXPERIMENT ================= */

int main() {

    const int START_SIZE = 10000;
    const int MAX_SIZE   = 500000;
    const int STEP_SIZE  = 5000;

    const int TRIALS = 20;        // Number of trials per size
    const int WARMUP_RUNS = 5;    // Warm-up runs

    mt19937 rng(1337);

    ofstream file("quicksort_avg_case.csv");
    file << "Size,Avg_Time_ms,N_logN\n";

    for (int size = START_SIZE; size <= MAX_SIZE; size += STEP_SIZE) {

        uniform_int_distribution<int> dist(0, size * 10);

        // -------- Warm-up Phase --------
        for (int w = 0; w < WARMUP_RUNS; ++w) {
            vector<int> warm_arr(size);
            for (int i = 0; i < size; ++i)
                warm_arr[i] = dist(rng);
            quick_sort(warm_arr, 0, size - 1);
        }

        // -------- Actual Measurement --------
        double total_time_micro = 0.0;

        for (int t = 0; t < TRIALS; ++t) {

            vector<int> arr(size);
            for (int i = 0; i < size; ++i)
                arr[i] = dist(rng);

            auto start = high_resolution_clock::now();
            quick_sort(arr, 0, size - 1);
            auto end = high_resolution_clock::now();

            total_time_micro += duration_cast<microseconds>(end - start).count();
        }

        // Convert microseconds to milliseconds
        double avg_time_ms = (total_time_micro / TRIALS) / 1000.0;

        double nlogn = size * log2(size);

        cout << "Size=" << size
             << " | Avg Time=" << fixed << setprecision(4)
             << avg_time_ms << " ms" << endl;

        file << size << "," << avg_time_ms << "," << nlogn << "\n";
    }

    file.close();
    return 0;
}
