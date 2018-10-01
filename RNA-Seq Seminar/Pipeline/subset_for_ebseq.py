# Short script
# Goal is to read in the Count_Matrix file
# Filter out the KO samples and sort the columns


import os;
import pandas as pd;

count_matrix = pd.read_table("Count_Matrix.txt", index_col=0, header=0)
count_matrix.index.name = "" # Need this so R reads it properly

sample_meta = pd.read_table("sample_meta.txt", index_col=0, header=0)


sample_meta = sample_meta.loc[sample_meta['Genotype'] == "WT"]
sample_meta = sample_meta.sort_values("Stimulus")

count_matrix = count_matrix[sample_meta.index]

sample_meta.to_csv("sample_meta_ebseq.txt", sep="\t");

count_matrix.to_csv("count_matrix_ebseq.txt", sep="\t");
