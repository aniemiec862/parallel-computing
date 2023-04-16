#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=00:05:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

module add gcc/10.3.0

g++ -std=c++11 -fopenmp -o sort sort.cpp

for i in {1..48}
do
    ./sort_sync 33554432 $i {$bucket_size} 3
done
