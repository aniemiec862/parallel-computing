#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main (int argc, char* argv[]) {
    int num_threads = atoi(argv[1]);
    unsigned long long array_size = strtoull(argv[2], NULL, 10);

    double* array = (double*) malloc(sizeof(double) * array_size);
    double start_time, end_time;
    start_time = omp_get_wtime();

    #pragma omp parallel num_threads(num_threads)
    {
        unsigned short xi[3];
        xi[0] = (unsigned short)time(NULL) + omp_get_thread_num();
        xi[1] = (unsigned short)(time(NULL) >> 16) + omp_get_thread_num();
        xi[2] = 0;

        #pragma omp for
        for (unsigned long long i = 0; i < array_size; i++) {
            array[i] = erand48(xi);
        }
    }
    end_time = omp_get_wtime();
    printf("%d;%f;%d\n", num_threads, end_time - start_time, array_size);

    free(array);
    return 0;
}
