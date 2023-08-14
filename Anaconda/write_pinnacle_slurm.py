#! usr/bin/env python3

# import modules
import argparse

# create argument parser object
parser = argparse.ArgumentParser(description='This script returns a SLURM script with the passed arguments and options')

# add positional arguments
parser.add_argument('job', help = 'The name of the SLURM job', type = str)

# add optional arguments
parser.add_argument('-q', '-queue', help = 'Which HPC queue to utilize', default = 'comp72', type = str)
parser.add_argument('-nodes', help = 'Number of HPC nodes to utilize on job', default = 1, type = int)
parser.add_argument('-processors', help = 'Number of HPC processors to utilize on job', default = 1, type = int)
parser.add_argument('-walltime', help = 'Max time allotted for job', default = 1, type = int)

# parse arguments
args = parser.parse_args()

# Variables

job_name = args.job
queue = args.q
walltime = args.nodes
num_nodes = args.processors
num_processors = args.walltime

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

print()

print('# job command here')