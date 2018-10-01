#!/usr/bin/env python
from __future__ import print_function, division
import time
import os
import sys
import subprocess as sp;
import pandas as pd;

RSEM_LOCATION = ''
RSEM_REFERENCE = "/home/deto/References/Homo_sapiens/Ensemble/GRCh38/hg38_rsem"
REFFLAT_FILE = "/home/deto/References/Homo_sapiens/Ensemble/GRCh38/refFlat_fixed.txt"


def gzip(inFile):
    """
    Runs gzip on a file and returns the new file name
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
    """

    if not inFile.endswith(".gz"):
        return inFile  # Already deflated

    sp.call(["gzip", "-d", inFile]);

    outFile = inFile[0:inFile.rfind(".gz")];
    if not os.path.isfile(outFile):
        raise Exception("Error GZIPping", outFile);

    return outFile;


def runRSEM(readFile, outputDir):
    """
    Runs RSEM on a fastq files of reads to align transcripts
    Returns the folder with the RSEM results

    If readFile is a tuple, we run paired-end rsem
    """

    if not os.path.isdir(outputDir):
        os.makedirs(outputDir);

    rsem_output = os.path.join(outputDir, "results");

    command = [os.path.join(RSEM_LOCATION, "rsem-calculate-expression"),
        "--paired-end",
        readFile[0], readFile[1],
        "--bowtie2",
        "--output-genome-bam",
        "--sort-bam-by-coordinate",
        RSEM_REFERENCE,
        rsem_output];

    print(" ".join(command));
    sp.call(command);

    return rsem_output;


def runPicardQC(directory):
    """
    Runs Picard on an aligment to generate Quality indicators
    Returns the folder with the Picard results
    """
    # Run CollectRnaSeqMetrics
    command = ["java", "-jar", "$PICARD", "CollectRnaSeqMetrics",
            "I=" + os.path.join(directory, 'results.genome.sorted.bam'),
            "O=" + os.path.join(directory, "CollectRnaSeqMetrics.txt"),
            "REF_FLAT=" + REFFLAT_FILE,
            "STRAND=NONE"]

    command = " ".join(command)
    print(command)

    sp.call(command, shell=True);

    # Run CollectInsertSizeMetrics
    command = ["java", "-jar", "$PICARD", "CollectInsertSizeMetrics",
            "I=" + os.path.join(directory, 'results.genome.sorted.bam'),
            "O=" + os.path.join(directory, 'CollectInsertSizeMetrics.txt'),
            "H=" + os.path.join(directory, 'CollectInsertSizeMetrics.pdf')]

    command = " ".join(command)
    print(command)

    sp.call(command, shell=True);

    # Collect the results into one file
    metrics = pd.Series();
    with open('CollectRnaSeqMetrics.txt', 'r') as fin:
        lines = fin.readlines()
        for i, line in enumerate(lines):
            if line.startswith('## METRICS'):
                headers = lines[i + 1][:-1].split("\t")
                values = lines[i + 2][:-1].split("\t")
                for header, value in zip(headers, values):
                    try:
                        floatval = float(value)
                        metrics[header] = float(value)
                    except ValueError:
                        pass

                break;

    with open('CollectInsertSizeMetrics.txt', 'r') as fin:
        lines = fin.readlines()
        for i, line in enumerate(lines):
            if line.startswith('## METRICS'):
                headers = lines[i + 1][:-1].split("\t")
                values = lines[i + 2][:-1].split("\t")
                for header, value in zip(headers, values):
                    try:
                        floatval = float(value)
                        metrics[header] = floatval
                    except ValueError:
                        pass

                break;

    metrics.to_csv("QC.txt", sep="\t")

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

fastqPair = (sample1, sample2)

rsem_output_dir = os.path.join(folder, "RSEM_Out");
print(rsem_output_dir)

runRSEM(fastqPair, rsem_output_dir)
runPicardQC(rsem_output_dir)

stop_time = time.time()

print("Elapsed (seconds): ", stop_time - start_time)

sample1 = gzip(sample1);
sample2 = gzip(sample2);
