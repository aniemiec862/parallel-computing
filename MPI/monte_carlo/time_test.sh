#!/bin/bash -l
#SBATCH --nodes 1
#SBATCH --ntasks 12
#SBATCH --time=12:00:00
#SBATCH --partition=plgrid
#SBATCH --account=plgmpr23-cpu

module add scipy-bundle/2021.10-foss-2021b

mpiexec -np 1 ./pi.py 1000000
mpiexec -np 1 ./pi.py 750000
mpiexec -np 1 ./pi.py 500000

mpiexec -np 12 ./pi.py 50000000
mpiexec -np 12 ./pi.py 100000000
mpiexec -np 12 ./pi.py 200000000