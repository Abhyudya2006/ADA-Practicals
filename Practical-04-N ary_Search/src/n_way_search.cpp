#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <fstream>
#include <iomanip>

using namespace std;
using namespace std::chrono;

// N-ary Search Implementation
int nary_search(const vector<int>& arr, int target, int n) {
    int low = 0, high = arr.size() - 1;
    while (low <= high) {
        if (n < 2) n = 2;
        if ((high - low) < n) {
            for (int i = low; i <= high; ++i) if (arr[i] == target) return i;
            return -1;
        }
        
        vector<int> boundaries;
        boundaries.reserve(n - 1);
        double step = static_cast<double>(high - low) / n;
        for (int i = 1; i < n; ++i) {
            boundaries.push_back(low + static_cast<int>(i * step));
        }

        for (int b_idx : boundaries) if (arr[b_idx] == target) return b_idx;

        if (target < arr[boundaries[0]]) {
            high = boundaries[0] - 1;
        } else if (target > arr[boundaries.back()]) {
            low = boundaries.back() + 1;
        } else {
            for (size_t i = 0; i < boundaries.size() - 1; ++i) {
                if (target > arr[boundaries[i]] && target < arr[boundaries[i + 1]]) {
                    low = boundaries[i] + 1;
                    high = boundaries[i + 1] - 1;
                    break;
                }
            }
        }
    }
    return -1;
}

int main() {
    const int SIZE = 5000000;
    const int ITERATIONS = 500000; 
    const vector<int> n_values = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21};

    vector<int> test_array(SIZE);
    mt19937 rng(1337); 
    uniform_int_distribution<int> dist(0, SIZE * 2); 

    for (int i = 0; i < SIZE; ++i) test_array[i] = dist(rng);
    sort(test_array.begin(), test_array.end());

    for (int i = 0; i < 200000; ++i) nary_search(test_array, dist(rng), 2);

    ofstream file("nary_results_3.csv");
    file << "N,Time_ns\n";

    for (int n : n_values) {

        mt19937 search_rng(42); 
        
        auto start = high_resolution_clock::now();
        for (int i = 0; i < ITERATIONS; ++i) {
            int target = dist(search_rng); //random target
            nary_search(test_array, target, n);
        }
        auto end = high_resolution_clock::now();
        
        double avg_ns = duration_cast<nanoseconds>(end - start).count() / (double)ITERATIONS;
        cout << "N=" << n << " | " << fixed << setprecision(2) << avg_ns << " ns" << endl;
        file << n << "," << avg_ns << "\n";
    }

    file.close();
    return 0;
}