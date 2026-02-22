#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <fstream>
#include <iomanip>
#include <algorithm>
#include <cmath>
#include <thread>

using namespace std;
using namespace std::chrono;

/* ================= FIRST PIVOT ================= */

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

void quicksort_first(vector<int>& arr, int low, int high) {
    while (low < high) {   // tail recursion optimization
        int p = partition_first(arr, low, high);

        if (p - low < high - p) {
            quicksort_first(arr, low, p - 1);
            low = p + 1;
        } else {
            quicksort_first(arr, p + 1, high);
            high = p - 1;
        }
    }
}

/* ================= RANDOM PIVOT ================= */

int partition_random(vector<int>& arr, int low, int high, mt19937& rng) {
    uniform_int_distribution<int> dist(low, high);
    int random_index = dist(rng);
    swap(arr[low], arr[random_index]);
    return partition_first(arr, low, high);
}

void quicksort_random(vector<int>& arr, int low, int high, mt19937& rng) {
    if (low < high) {
        int p = partition_random(arr, low, high, rng);
        quicksort_random(arr, low, p - 1, rng);
        quicksort_random(arr, p + 1, high, rng);
    }
}

/* ================= MAIN ================= */

int main() {

    const int START_SIZE = 10000;
    const int MAX_SIZE   = 100000;
    const int STEP_SIZE  = 5000;

    const int TRIALS_FIRST  = 1;   // quadratic version (heavy)
    const int TRIALS_RANDOM = 20;   // lighter version
    const int WARMUP_RUNS = 2;

    mt19937 rng(1337);

    ofstream file("quicksort_worst_case.csv");
    file << "Size,FirstPivot_ms,RandomPivot_ms,N_squared,N_logN\n";

    vector<double> first_results;
    vector<double> random_results;
    vector<int> sizes_record;

    /* ================= FIRST PIVOT TEST ================= */

    cout << "Running First Pivot (Worst Case)...\n";

    for (int size = START_SIZE; size <= MAX_SIZE; size += STEP_SIZE) {

        uniform_int_distribution<int> dist(0, size * 10);

        // Warmup
        for (int w = 0; w < WARMUP_RUNS; ++w) {
            vector<int> warm(size);
            for (int i = 0; i < size; ++i)
                warm[i] = dist(rng);
            sort(warm.begin(), warm.end());
            quicksort_first(warm, 0, size - 1);
        }

        double total_first = 0.0;

        for (int t = 0; t < TRIALS_FIRST; ++t) {

            vector<int> arr(size);
            for (int i = 0; i < size; ++i)
                arr[i] = dist(rng);

            sort(arr.begin(), arr.end());

            auto start = high_resolution_clock::now();
            quicksort_first(arr, 0, size - 1);
            auto end = high_resolution_clock::now();

            total_first += duration_cast<microseconds>(end - start).count();
        }

        double avg_first = (total_first / TRIALS_FIRST) / 1000.0;

        first_results.push_back(avg_first);
        sizes_record.push_back(size);

        cout << "Size=" << size << " | FirstPivot=" << avg_first << " ms\n";
    }

    // Cooldown
    this_thread::sleep_for(milliseconds(500));

    /* ================= RANDOM PIVOT TEST ================= */

    cout << "\nRunning Random Pivot...\n";

    for (int idx = 0; idx < sizes_record.size(); ++idx) {

        int size = sizes_record[idx];
        uniform_int_distribution<int> dist(0, size * 10);

        double total_random = 0.0;

        for (int t = 0; t < TRIALS_RANDOM; ++t) {

            vector<int> arr(size);
            for (int i = 0; i < size; ++i)
                arr[i] = dist(rng);

            sort(arr.begin(), arr.end());

            auto start = high_resolution_clock::now();
            quicksort_random(arr, 0, size - 1, rng);
            auto end = high_resolution_clock::now();

            total_random += duration_cast<microseconds>(end - start).count();
        }

        double avg_random = (total_random / TRIALS_RANDOM) / 1000.0;
        random_results.push_back(avg_random);

        cout << "Size=" << size << " | RandomPivot=" << avg_random << " ms\n";
    }

    /* ================= WRITE TO FILE ================= */

    for (int i = 0; i < sizes_record.size(); ++i) {
        int size = sizes_record[i];
        double n_squared = size * size;
        double nlogn = size * log2(size);

        file << size << ","
             << first_results[i] << ","
             << random_results[i] << ","
             << n_squared << ","
             << nlogn << "\n";
    }

    file.close();
    return 0;
}
