#! usr/bin/env python3

# import modules
import argparse

# create argument parser object
parser = argparse.ArgumentParser(description='This script returns a SLURM script with the passed arguments and options')

# add positional arguments
parser.add_argument('job', help = 'The name of the SLURM job', type = str)

# add optional arguments
parser.add_argument('-q', '--queue', help = 'Which HPC queue to utilize', default = 'comp72', type = str)
parser.add_argument('-n', '--nodes', help = 'Number of HPC nodes to utilize on job', default = 1, type = int)
parser.add_argument('-p', '--processors', help = 'Number of HPC processors to utilize on job', default = 1, type = int)
parser.add_argument('-w', '--walltime', help = 'Max time allotted for job', default = 1, type = int)
parser.add_argument('-f', '--file', help = 'Send to a file in the script\'s directory with the given name', type = str)
parser.add_argument('-d', '--directory', help = 'Send a file to the given path/name - overrides --file option', type = str)

# parse arguments
args = parser.parse_args()

# Variables

job_name = args.job
queue = args.queue
walltime = args.nodes
num_nodes = args.processors
num_processors = args.walltime

if args.directory:
    with open(args.directory, 'w') as f:
        f.write('#!/bin/bash' + '\n')

        f.write('\n')

        f.write('#SBATCH --job-name=' + job_name + '\n')
        f.write('#SBATCH --partition ' + queue + '\n')
        f.write('#SBATCH --nodes=' + str(num_nodes) + '\n')
        f.write('#SBATCH --qos comp' + '\n')
        f.write('#SBATCH --tasks-per-node=' + str(num_processors) + '\n')
        f.write('#SBATCH --time=' + str(walltime) + ':00:00' + '\n')
        f.write('#SBATCH -o test_%j.out' + '\n')
        f.write('#SBATCH -e test_%j.err' + '\n')
        f.write('#SBATCH --mail-type=ALL' + '\n')
        f.write('#SBATCH --mail-user=email@uark.edu' + '\n')

        f.write('\n')

        f.write('module purge' + '\n')

        f.write('\n')

        f.write('cd $SLURM_SUBMIT_DIR' + '\n')

        f.write('\n' + '\n')

        f.write('# job command here' + '\n')
elif args.file:
    with open(args.file, 'w') as f:
        f.write('#!/bin/bash' + '\n')

        f.write('\n')

        f.write('#SBATCH --job-name=' + job_name + '\n')
        f.write('#SBATCH --partition ' + queue + '\n')
        f.write('#SBATCH --nodes=' + str(num_nodes) + '\n')
        f.write('#SBATCH --qos comp' + '\n')
        f.write('#SBATCH --tasks-per-node=' + str(num_processors) + '\n')
        f.write('#SBATCH --time=' + str(walltime) + ':00:00' + '\n')
        f.write('#SBATCH -o test_%j.out' + '\n')
        f.write('#SBATCH -e test_%j.err' + '\n')
        f.write('#SBATCH --mail-type=ALL' + '\n')
        f.write('#SBATCH --mail-user=email@uark.edu' + '\n')

        f.write('\n')

        f.write('module purge' + '\n')

        f.write('\n')

        f.write('cd $SLURM_SUBMIT_DIR' + '\n')

        f.write('\n' + '\n')

        f.write('# job command here' + '\n')
else:
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