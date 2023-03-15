#include "definitions.h"

double sender(int msg_size);

double sender(int msg_size) {
    char *buff = malloc(msg_size);
    int i;
    double start = MPI_Wtime();
    for (i = 0; i < N; i++) {
        MPI_Send(buff, msg_size, MPI_BYTE, RECEIVER, 0, MPI_COMM_WORLD);
        MPI_Recv(buff, msg_size, MPI_BYTE, RECEIVER, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    return MPI_Wtime() - start;
}

void receiver(int msg_size) {
    char *buff = malloc(msg_size);
    int i;
    for (i = 0; i < N; i++) {
        MPI_Recv(buff, msg_size, MPI_BYTE, SENDER, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Send(buff, msg_size, MPI_BYTE, SENDER, 0, MPI_COMM_WORLD);
    }
}

void test(long msg_size, int rank) {
    if (rank == SENDER) {
        double time = sender(msg_size);
        printf("%d;%f  \n", msg_size, N*msg_size/(64*1024*time));
    } else if (rank == RECEIVER) {
        receiver(msg_size);
    }
}

int main(int argc, char *argv[]) {

    MPI_Init(&argc, &argv);

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    long msg_size = argv[1];
    test(msg_size, rank);

    MPI_Finalize();
    return 0;
}
