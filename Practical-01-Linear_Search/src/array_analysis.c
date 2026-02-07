#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ARRAY_SIZE 1000000
#define MAX_VALUE  (2*ARRAY_SIZE)
#define BUCKETS    10

int cmp(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

void generate_array(int* arr, int n) {
    for (int i = 0; i < n; i++) {
        arr[i] = (int)(((unsigned long long)rand() << 15 | rand()) % MAX_VALUE);
    }
}

void analyze_duplicates(const int* arr, int n,
                        int* unique, int* duplicates) {

    *unique = 1;
    *duplicates = 0;

    for (int i = 1; i < n; i++) {
        if (arr[i] == arr[i - 1])
            (*duplicates)++;
        else
            (*unique)++;
    }
}

void analyze_stats(const int* arr, int n,
                   int* min, int* max, double* mean) {

    long long sum = 0;
    *min = arr[0];
    *max = arr[n - 1];

    for (int i = 0; i < n; i++)
        sum += arr[i];

    *mean = (double)sum / n;
}

void analyze_histogram(const int* arr, int n, int* bucket) {
    for (int i = 0; i < BUCKETS; i++)
        bucket[i] = 0;

    for (int i = 0; i < n; i++) {
        int index = (int)((long long)arr[i] * BUCKETS / MAX_VALUE);
        if (index >= BUCKETS) index = BUCKETS - 1;
        bucket[index]++;
    }
}

int main() {
    srand((unsigned)time(NULL));

    int* arr = (int*)malloc(sizeof(int) * ARRAY_SIZE);

    generate_array(arr, ARRAY_SIZE);

    qsort(arr, ARRAY_SIZE, sizeof(int), cmp);

    int unique, duplicates;
    analyze_duplicates(arr, ARRAY_SIZE, &unique, &duplicates);

    int min, max;
    double mean;
    analyze_stats(arr, ARRAY_SIZE, &min, &max, &mean);

    int bucket[BUCKETS];
    analyze_histogram(arr, ARRAY_SIZE, bucket);

    printf("\nARRAY / RANDOM NUMBER ANALYSIS\n");
    printf("-------------------------------------------------\n");
    printf("Array Size           : %d\n", ARRAY_SIZE);
    printf("Unique Elements      : %d\n", unique);
    printf("Duplicate Elements   : %d\n", duplicates);
    printf("Duplicate %%          : %.2f%%\n",
           (double)duplicates / ARRAY_SIZE * 100);
    printf("Min Value            : %d\n", min);
    printf("Max Value            : %d\n", max);
    printf("Mean Value           : %.2f\n", mean);

    printf("\nHistogram (Uniformity Check):\n");
    for (int i = 0; i < BUCKETS; i++) {
        printf("Bucket %d : %d\n", i, bucket[i]);
    }

    printf("-------------------------------------------------\n");

    free(arr);
    return 0;
}
