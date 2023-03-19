#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=00:10:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

module add scipy-bundle/2021.10-foss-2021b

mpiexec -np 1 ./mc.py 100000
mpiexec -np 1 ./mc.py 200000
mpiexec -np 1 ./mc.py 250000

mpiexec -np 12 ./mc.py 1000000000
mpiexec -np 12 ./mc.py 1250000000
mpiexec -np 12 ./mc.py 1500000000
