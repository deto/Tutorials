from __future__ import print_function, division
import os
import sys
import subprocess as sp;


current_directory = os.path.dirname(os.path.abspath(__file__))
processPairCommand = os.path.join(current_directory, 'processSamplePair_withQC.py')


def getFastqFiles(folder):
    """
    Returns a list of the fastq files in a directory
    """
    all_files = os.listdir(folder)

    fastq_files = []
    for filename in all_files:
        if '.fastq' in filename.lower():
            fastq_files.append(os.path.join(folder, filename))

    return fastq_files


def getSampleName(fastq_file):
    """
    Parses the fastq file name for a sample name
    """
    basename = os.path.basename(fastq_file[0]);  # Strips off the folders
    rootname = basename[0:basename.find("_1")];  # Gets everything before the _1
    return rootname


def gatherFastqPairs(file_names):
    """
    Returns a list of 2-tuples with corresponding up and downstream
    read files
    """
    fastqPairs = [];
    for filename in file_names:
        if "_1" in filename:
            pair_file = filename.replace("_1", "_2");
            fastqPairs.append((filename, pair_file));

    return fastqPairs;

# main loop
if __name__ == "__main__":
    folder = sys.argv[1]
    folder = os.path.abspath(folder)

    fastq_files = getFastqFiles(folder)
    fastq_pairs = gatherFastqPairs(fastq_files);

    records = []
    for fastqPair in fastq_pairs:
        record = {}
        record['name'] = getSampleName(fastqPair)

        os.mkdir(record['name']);

        errFile = open(os.path.join(record['name'], 'err.txt'), 'w');
        logFile = open(os.path.join(record['name'], 'log.txt'), 'w');

        sp.Popen(["python", processPairCommand, record['name'], fastqPair[
                 0], fastqPair[1]], stdout=logFile, stderr=errFile);
        print("Running ", record['name'])
