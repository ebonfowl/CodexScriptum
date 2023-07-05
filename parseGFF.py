#! usr/bin/env python3

# import modules
import argparse
import csv
from Bio import SeqIO

# create argument parser object
parser = argparse.ArgumentParser(description = 'This script reads in a GFF file line by line')

# add positional arguments
parser.add_argument('gff_file', help = 'GFF filepath', type = str)
parser.add_argument('fasta_file', help = 'FASTA filepath', type = str)

# parse arguments
args = parser.parse_args()

genome = SeqIO.read(args.fasta_file, "fasta")
# print(genome)

# read file
GFF_file = open(args.gff_file, 'r')

reader = csv.reader(GFF_file, delimiter = '\t')

for line in reader:

    if not line:
        continue

    # define column variables
    organism = line[0]
    source = line[1]
    feature_type = line[2]
    start = int(line[3])
    end = int(line[4])

    # fix length
    line[5] = str(end - start + 1)

    length = line[5]
    strand = line[6]
    attributes = line[8]

    # print(feature_type + '\t' + length)

    sequence = genome.seq[start - 1: end]
    # header = ' '.join(organism, feature_type, attributes)
    print('>' + organism, feature_type, attributes)
    print(sequence)

GFF_file.close()