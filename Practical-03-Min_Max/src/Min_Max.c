#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

#define START_SIZE   10000
#define END_SIZE     2000000
#define STEP_SIZE    20000
#define SEARCHES     3000

void find_max_min_independent(int *arr, int n) {
    int max = arr[0], min = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) max = arr[i];
        if (arr[i] < min) min = arr[i];
    }
}

void find_max_min_ifelse(int *arr, int n) {
    int max = arr[0], min = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] > max) {
            max = arr[i];
        } else if (arr[i] < min) {
            min = arr[i];
        }
    }
}

int main() {
    LARGE_INTEGER freq, start, end;
    QueryPerformanceFrequency(&freq);
    srand(time(NULL));
    
    FILE *fout = fopen("max_min_comparison.csv", "w");
    fprintf(fout, "Size,IndependentTime,IfElseTime\n");

    printf("%-10s | %-15s | %-15s | %-10s\n", "Size", "Independent", "If-Else", "Difference");
    printf("----------------------------------------------------------------------\n");

    for (int n = START_SIZE; n <= END_SIZE; n += STEP_SIZE) {
        int *arr = (int *)malloc(n * sizeof(int));
        for (int i = 0; i < n; i++) arr[i] = rand();

        // Measurement for Independent Ifs
        QueryPerformanceCounter(&start);
        for (int i = 0; i < SEARCHES; i++) find_max_min_independent(arr, n);
        QueryPerformanceCounter(&end);
        double t1 = (double)(end.QuadPart - start.QuadPart) / (freq.QuadPart * SEARCHES);

        // Measurement for If-Else Clause
        QueryPerformanceCounter(&start);
        for (int i = 0; i < SEARCHES; i++) find_max_min_ifelse(arr, n);
        QueryPerformanceCounter(&end);
        double t2 = (double)(end.QuadPart - start.QuadPart) / (freq.QuadPart * SEARCHES);

        // Print to Terminal
        printf("%-10d | %-15.10f | %-15.10f | %-10.2f%%\n", 
               n, t1, t2, ((t1 - t2) / t1) * 100);

        // Save to CSV
        fprintf(fout, "%d,%.10f,%.10f\n", n, t1, t2);
        
        free(arr);
    }
    fclose(fout);
    printf("----------------------------------------------------------------------\n");
    printf("Data saved to max_min_comparison.csv\n");
    return 0;
}