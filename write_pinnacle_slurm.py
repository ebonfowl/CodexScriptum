#! usr/bin/env python3

# Variables

job_name = '<JOB-NAME>'
queue = 'comp01'
walltime = 1
num_nodes = 1
num_processors = 24

print('#!/bin/bash')

print()

print('#SBATCH --job-name=' + job_name)
print('#SBATCH --partition ' + queue)
print('#SBATCH --nodes=' + str(num_nodes))
print('#SBATCH --qos comp')
print('#SBATCH --tasks-per-node=' + str(num_processors))
print('#SBATCH --time=' + str(walltime) + ':00:00')
print('#SBATCH -o test_%j.out')
print('#SBATCH -e test_%j.err')
print('#SBATCH --mail-type=ALL')
print('#SBATCH --mail-user=email@uark.edu')

print()

print('module purge')

print()

print('cd $SLURM_SUBMIT_DIR')
print('# job command here')