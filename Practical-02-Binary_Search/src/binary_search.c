#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

/* ---------------- CONFIG ---------------- */
#define START_SIZE   10000
#define END_SIZE     10000000
#define STEP_SIZE    5000
#define SEARCHES     40000
#define MAX_VALUE    (2 * END_SIZE)

/* ---------------- ARRAY STRUCT ---------------- */
typedef struct {
    int *data;
    int size;
} Array;

/* ---------------- COMPARATOR ---------------- */
int cmp(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

/* ---------------- ARRAY GENERATION ---------------- */
int get_large_rand() {
    return (int)(((unsigned long long)rand() << 15 | rand()) % MAX_VALUE);
}

Array create_array(int n) {
    Array a;
    a.size = n;
    a.data = (int *)malloc(sizeof(int) * n);
    for (int i = 0; i < n; i++) {
        a.data[i] = get_large_rand();
    }
    qsort(a.data, n, sizeof(int), cmp);
    return a;
}

void free_array(Array *a) {
    if (a->data) {
        free(a->data);
    }
    a->data = NULL;
    a->size = 0;
}

/* ---------------- BINARY SEARCH ---------------- */
int binary_search(const Array *a, int key) {
    int low = 0, high = a->size - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (a->data[mid] == key)
            return mid;
        else if (a->data[mid] < key)
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;
}

/* ---------------- ANALYSIS ---------------- */
void run_average_case(FILE *fout, const Array *a, LARGE_INTEGER freq) {
    int hits = 0, misses = 0;
    double index_sum = 0;

    LARGE_INTEGER start, end;
    QueryPerformanceCounter(&start);

    for (int i = 0; i < SEARCHES; i++) {
        int key = get_large_rand();
        int pos = binary_search(a, key);
        if (pos != -1) {
            hits++;
            index_sum += (double)pos;
        } else {
            misses++;
        }
    }

    QueryPerformanceCounter(&end);

    double total_time = (double)(end.QuadPart - start.QuadPart) / freq.QuadPart;
    double avg_time = total_time / SEARCHES;
    double avg_index = (hits > 0) ? (index_sum / hits) : 0.0;

    /* CSV OUTPUT: Size, Hits, Misses, HitPercent, AvgTime, AvgFoundIndex */
    fprintf(fout, "%d,%d,%d,%.2f,%.10f,%.2f\n",
            a->size, hits, misses, (double)hits / SEARCHES * 100, avg_time, avg_index);

    printf("Size: %d | Time: %.10f | Hits: %d | Index: %.2f\n", a->size, avg_time, hits, avg_index);
}

int main() {
    srand((unsigned)time(NULL));
    LARGE_INTEGER freq;
    QueryPerformanceFrequency(&freq);

    FILE *fout = fopen("binary_search_results3.csv", "w");
    fprintf(fout, "ArraySize,Hits,Misses,HitPercent,AvgTime,AvgFoundIndex\n");

    printf("BINARY SEARCH - SYSTEM ANALYSIS\n");
    printf("==================================================\n");

    for (int n = START_SIZE; n <= END_SIZE; n += STEP_SIZE) {
        Array arr = create_array(n);
        run_average_case(fout, &arr, freq);
        free_array(&arr);
    }

    fclose(fout);
    return 0;
}