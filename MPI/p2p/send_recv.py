#!/usr/bin/env python
from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

test_count = 100
bytes_to_send = int(sys.argv[1])
message = "A" * bytes_to_send
res = []

def ping_pong():
    comm.Barrier()
    start = MPI.Wtime()

    if rank == 0:
        comm.send(message, dest=1)
        comm.recv(source=1)
    elif rank == 1:
        data = comm.recv(source=0)
        comm.send(data, dest=0)

    stop = MPI.Wtime()

    return (stop - start) / 2

summed_time = 0

for i in range(test_count):
    time = ping_pong()
    summed_time = summed_time + time

if rank == 0:
    result = summed_time / test_count
    res.sort()
    median = (res[50]+res[51])/2
    speed_in_mega_bits = (bytes_to_send * 8 / median) / 1000000

    output = "{bytes};{speed}".format(bytes=bytes_to_send, speed=speed_in_mega_bits)
    print output
