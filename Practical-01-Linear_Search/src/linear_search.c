#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

#define START_SIZE  10000
#define END_SIZE    5000000
#define STEP_SIZE   50000

#define SEARCHES    2500
#define MAX_VALUE  (2*END_SIZE)

typedef struct {
    int* data;
    int size;
} Array;

Array create_array(int n) {
    Array a;
    a.size = n;
    a.data = (int*)malloc(sizeof(int) * n);

    for (int i = 0; i < n; i++) {
        a.data[i] =
            (int)(((unsigned long long)rand() << 15 | rand()) % MAX_VALUE);
    }
    return a;
}

void free_array(Array* a) {
    free(a->data);
    a->data = NULL;
    a->size = 0;
}

int linear_search(const Array* a, int key) {
    for (int i = 0; i < a->size; i++) {
        if (a->data[i] == key)
            return i;
    }
    return -1;
}

void run_average_case(FILE* fhit,
                      FILE* fmiss,
                      FILE* ftime,
                      FILE* findex,
                      const Array* a,
                      LARGE_INTEGER freq) {

    int hits = 0, misses = 0;
    long long index_sum = 0;

    LARGE_INTEGER start, end;
    QueryPerformanceCounter(&start);

    for (int i = 0; i < SEARCHES; i++) {
        int idx = rand() % a->size;
        int key = rand() % MAX_VALUE;

        int pos = linear_search(a, key);
        if (pos != -1) {
            hits++;
            index_sum += pos;
        } else {
            misses++;
        }
    }

    QueryPerformanceCounter(&end);

    double avg_time =
        (double)(end.QuadPart - start.QuadPart)
        / freq.QuadPart / SEARCHES;

    double avg_index =
        (hits > 0) ? (double)index_sum / hits : -1;

    fprintf(fhit,  "%d,%d,%.2f\n",
             a->size, hits, (double)hits / SEARCHES * 100);

    fprintf(fmiss, "%d,%d,%.2f\n",
             a->size, misses, (double)misses / SEARCHES * 100);

    fprintf(ftime, "%d,%.10f\n",
             a->size, avg_time);

    fprintf(findex, "%d,%.2f\n",
             a->size, avg_index);

    printf("Array Size        : %d\n", a->size);
    printf("Hits              : %d (%.2f%%)\n",
           hits, (double)hits / SEARCHES * 100);
    printf("Misses            : %d (%.2f%%)\n",
           misses, (double)misses / SEARCHES * 100);
    printf("Avg Found Index   : %.2f (Expected ~ %.2f)\n",
           avg_index, a->size / 2.0);
    printf("Avg Search Time   : %.10f sec\n", avg_time);
    printf("--------------------------------------------------\n");
}

int main() {
    srand((unsigned)time(NULL));

    LARGE_INTEGER freq;
    QueryPerformanceFrequency(&freq);

    FILE* fhit   = fopen("linear_hits3.csv", "w");
    FILE* fmiss  = fopen("linear_misses3.csv", "w");
    FILE* ftime  = fopen("linear_time3.csv", "w");
    FILE* findex = fopen("linear_avg_index3.csv", "w"); 

    fprintf(fhit,   "ArraySize,Hits,HitPercent\n");
    fprintf(fmiss,  "ArraySize,Misses,MissPercent\n");
    fprintf(ftime,  "ArraySize,AvgTime\n");
    fprintf(findex, "ArraySize,AvgFoundIndex\n");

    printf("\nLINEAR SEARCH - AVERAGE CASE ANALYSIS\n");
    printf("==================================================\n");

    for (int n = START_SIZE; n <= END_SIZE; n += STEP_SIZE) {
        Array arr = create_array(n);
        run_average_case(fhit, fmiss, ftime, findex, &arr, freq);
        free_array(&arr);
    }

    fclose(fhit);
    fclose(fmiss);
    fclose(ftime);
    fclose(findex);

    return 0;
}
