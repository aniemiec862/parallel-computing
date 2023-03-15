#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>

#define SENDER 1
#define RECEIVER 0
#define N 2000
#define MAX_MESSAGE_SIZE 500000