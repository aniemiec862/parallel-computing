#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=04:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

module add gcc/10.3.0

g++ -std=c++11 -fopenmp -o sort sort.cpp

for i in {1..4}
do
    ./sort 33554432 $i 67108 10
done
