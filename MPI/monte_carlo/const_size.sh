#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=06:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

module add scipy-bundle/2021.10-foss-2021b

for totalPoints in 100000 11180339 1250000000
do
    for threads in {1..12}
    do
        for i in {1..10}
        do
            mpiexec -np $threads ./mc.py $totalPoints
        done
    done
done