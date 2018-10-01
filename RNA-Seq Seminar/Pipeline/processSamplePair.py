#!/usr/bin/env python
from __future__ import print_function, division
import time
import os
import sys
import subprocess as sp;

RSEM_LOCATION = ''
RSEM_REFERENCE = "/home/deto/References/Homo_sapiens/Ensemble/GRCh38/hg38_rsem"
REFFLAT_FILE = "/home/deto/References/Homo_sapiens/Ensemble/GRCh38/refFlat_fixed.txt"


def gzip(inFile):
    """
    Runs gzip on a file and returns the new file name
    If the file is already zipped, just returns the file name
    """
    if inFile.endswith(".gz"):
        return inFile;

    sp.call(["gzip", inFile]);

    outFile = inFile + ".gz"
    if not os.path.isfile(outFile):
        raise Exception("Error GZIPping", outFile);

    return outFile;


def ungzip(inFile):
    """
    Decompresses gzip file and returns the new file name
    If the file is already unzipped, just returns the file name
    """

    if not inFile.endswith(".gz"):
        return inFile  # Already deflated

    sp.call(["gzip", "-d", inFile]);

    outFile = inFile[0:inFile.rfind(".gz")];
    if not os.path.isfile(outFile):
        raise Exception("Error GZIPping", outFile);

    return outFile;


def runRSEM(readFile_1, readFile_2, outputDir):
    """
    Runs RSEM on a fastq files of reads to align transcripts
    Returns the folder with the RSEM results

    """

    if not os.path.isdir(outputDir):
        os.makedirs(outputDir);

    rsem_output = os.path.join(outputDir, "results");

    command = [os.path.join(RSEM_LOCATION, "rsem-calculate-expression"),
        "--paired-end",
        readFile_1, readFile_2,
        "--bowtie2",
        "--output-genome-bam",
        "--sort-bam-by-coordinate",
        RSEM_REFERENCE,
        rsem_output];

    print(" ".join(command));
    sp.call(command);

    return rsem_output;


start_time = time.time()

folder = sys.argv[1]
sample1 = sys.argv[2]
sample2 = sys.argv[3]

if(not os.path.exists(folder)):
    os.makedirs(folder)

folder = os.path.abspath(folder)
sample1 = os.path.abspath(sample1)
sample2 = os.path.abspath(sample2)

sample1 = ungzip(sample1);
sample2 = ungzip(sample2);

rsem_output_dir = os.path.join(folder, "RSEM_Out");

runRSEM(sample1, sample2, rsem_output_dir)

stop_time = time.time()

print("Elapsed (seconds): ", stop_time - start_time)

sample1 = gzip(sample1);
sample2 = gzip(sample2);
