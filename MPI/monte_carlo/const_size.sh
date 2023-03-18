#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=12:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

module add scipy-bundle/2021.10-foss-2021b

for totalPoints in 750000 21213203 600000000
do
    for threads in {1..12}
    do
        for i in {1..10}
        do
            mpiexec -np $threads ./pi.py $totalPoints
        done
    done
done