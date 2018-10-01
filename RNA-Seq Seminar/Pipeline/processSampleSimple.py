#!/usr/bin/env python
from __future__ import print_function, division
import time  # To tell us how long it took
import os  # To manipulate paths
import sys  # To get input arguments
import subprocess as sp  # To call other programs

RSEM_REFERENCE = "/home/deto/References/Homo_sapiens/Ensemble/GRCh38/hg38_rsem"

start_time = time.time()

folder = sys.argv[1]
sample1 = sys.argv[2]
sample2 = sys.argv[3]

folder = os.path.abspath(folder)
sample1 = os.path.abspath(sample1)
sample2 = os.path.abspath(sample2)

if(not os.path.exists(folder)):
    os.makedirs(folder)

sp.call(["gzip", "-d", sample1]);
sample1 = sample1[0:sample1.rfind(".gz")];

sp.call(["gzip", "-d", sample2]);
sample2 = sample2[0:sample2.rfind(".gz")];

rsem_output_dir = os.path.join(folder, "RSEM_Out");

command = ["rsem-calculate-expression",
    "--paired-end",
    sample1, sample2,
    "--bowtie2",
    "--output-genome-bam",
    "--sort-bam-by-coordinate",
    RSEM_REFERENCE,
    rsem_output_dir];

print(" ".join(command))
sp.call(command)

sp.call(["gzip", sample1])
sp.call(["gzip", sample2])

stop_time = time.time()

print("RSEM Complete!")
print("Elapsed (seconds): ", stop_time - start_time)

