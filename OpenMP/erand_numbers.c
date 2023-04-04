//Adam Niemiec, Michał Skwara

#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main (int argc, char* argv[]) {
    int num_threads = atoi(argv[1]);
    int array_size = atoi(argv[2]);

    double* array = (double*) malloc(sizeof(double) * array_size);
    double start_time, end_time;
    start_time = omp_get_wtime();

    #pragma omp parallel num_threads(num_threads)
    {
        unsigned short xi[3];
        xi[0] = 0;
        xi[1] = 0;
        xi[2] = 0;

        #pragma omp for schedule(static)
        for (int i = 0; i < array_size; i++) {
            array[i] = erand48(xi);
        }
    }
    end_time = omp_get_wtime();
    printf("%d;%f;%d\n", num_threads, end_time - start_time, array_size);

    free(array);
    return 0;
}
