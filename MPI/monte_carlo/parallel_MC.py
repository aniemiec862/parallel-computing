#!/usr/bin/env python
from mpi4py import MPI
import random
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
threads_number = comm.Get_size()


def get_random_point():
    return random.random(), random.random()


def is_inside(x, y):
    return (x ** 2 + y ** 2) < 1


points_to_generate = int(sys.argv[1])
points_inside = 0
points_per_node = points_to_generate // threads_number

comm.Barrier()
start = MPI.Wtime()

for _ in range(points_per_node):
    x, y = get_random_point()
    if is_inside(x, y):
        points_inside += 1

total_inside = comm.reduce(points_inside, op=MPI.SUM, root=0)
if rank == 0:
    result = 4 * (total_inside / points_to_generate)
    stop = MPI.Wtime()
    time = stop - start

    print(f"{points_to_generate};{threads_number};{time}")
