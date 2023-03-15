#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>

#define TAG 0

int compare_doubles(const void* a, const void* b) {
    double x = *(double*)a;
    double y = *(double*)b;
    return (x < y) ? -1 : ((x > y) ? 1 : 0);
}

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size, i;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int test_count = 100;
    int bytes_to_send = atoi(argv[1]);
    char* message = malloc(bytes_to_send + 1);
    memset(message, 'A', bytes_to_send);
    message[bytes_to_send] = '\0';

    double start, stop, time, summed_time = 0.0;
    double* res = malloc(sizeof(double) * test_count);

    for (i = 0; i < test_count; i++) {
        MPI_Barrier(MPI_COMM_WORLD);
        start = MPI_Wtime();

        if (rank == 0) {
            MPI_Send(message, bytes_to_send, MPI_CHAR, 1, TAG, MPI_COMM_WORLD);
            MPI_Recv(message, bytes_to_send, MPI_CHAR, 1, TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        } else if (rank == 1) {
            MPI_Recv(message, bytes_to_send, MPI_CHAR, 0, TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Send(message, bytes_to_send, MPI_CHAR, 0, TAG, MPI_COMM_WORLD);
        }

        stop = MPI_Wtime();
        time = (stop - start) / 2;
        res[i] = time;
        summed_time += time;
    }

    if (rank == 0) {
        double result = summed_time / test_count;
        double median;
        int middle = test_count / 2;

        // Sort the results array
        qsort(res, test_count, sizeof(double), compare_doubles);

        if (test_count % 2 == 0) {
            median = (res[middle - 1] + res[middle]) / 2;
        } else {
            median = res[middle];
        }

        double speed_in_mega_bits = (bytes_to_send * 8 / median) / 1000000;
        printf("%d;%f\n", bytes_to_send, speed_in_mega_bits);
    }

    MPI_Finalize();
    return 0;
}
