#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main (int argc, char* argv[]) {
    srand(time(NULL));

    int num_threads = atoi(argv[1]);
    unsigned long long array_size = strtoull(argv[2], NULL, 10);

    double* array = (double*) malloc(sizeof(double) * array_size);
    double start_time, end_time;
    start_time = omp_get_wtime();

    #pragma omp parallel num_threads(num_threads)
    {
        unsigned int seed = time(0) + omp_get_thread_num();

        #pragma omp for
        for(unsigned long long i=0 ; i < array_size ; i++){
            array[i] = (double)rand_r(&seed) / (double)RAND_MAX;
        }
    }
    end_time = omp_get_wtime();
    printf("%d;%f;%d\n", num_threads, end_time - start_time, array_size);

    free(array);
    return 0;
}
