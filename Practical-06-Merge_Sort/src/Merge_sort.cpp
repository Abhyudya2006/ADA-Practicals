#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <fstream>
#include <iomanip>
#include <cmath>

using namespace std;
using namespace std::chrono;

/* ================= MERGE SORT ================= */

void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; ++i)
        L[i] = arr[left + i];

    for (int j = 0; j < n2; ++j)
        R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j])
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];
    }

    while (i < n1)
        arr[k++] = L[i++];

    while (j < n2)
        arr[k++] = R[j++];
}

void merge_sort(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        merge_sort(arr, left, mid);
        merge_sort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

/* ================= MAIN EXPERIMENT ================= */

int main() {

    const int START_SIZE = 10000;
    const int MAX_SIZE   = 2000000;
    const int STEP_SIZE  = 50000;

    const int TRIALS = 5;
    const int WARMUP_RUNS = 5;

    mt19937 rng(1337);

    ofstream file("mergesort_avg_case_test.csv");
    file << "Size,Avg_Time_ms,N_logN\n";

    for (int size = START_SIZE; size <= MAX_SIZE; size += STEP_SIZE) {

        uniform_int_distribution<int> dist(0, size * 10);

        // -------- Warm-up Phase --------
        for (int w = 0; w < WARMUP_RUNS; ++w) {
            vector<int> warm_arr(size);
            for (int i = 0; i < size; ++i)
                warm_arr[i] = dist(rng);
            merge_sort(warm_arr, 0, size - 1);
        }

        // -------- Actual Measurement --------
        double total_time_micro = 0.0;

        for (int t = 0; t < TRIALS; ++t) {

            vector<int> arr(size);
            for (int i = 0; i < size; ++i)
                arr[i] = dist(rng);

            auto start = high_resolution_clock::now();
            merge_sort(arr, 0, size - 1);
            auto end = high_resolution_clock::now();

            total_time_micro += duration_cast<microseconds>(end - start).count();
        }

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