import os;
import pandas as pd;

def gatherResult(path_to_target, column_name, output_file_name):
    # Get all target_files
    target_files = []
    sample_names = []
    for dirname in os.listdir(os.getcwd()):
        if os.path.isdir(dirname):
            target_file = os.path.join(dirname, path_to_target)
            if os.path.isfile(target_file):
                target_files.append(target_file);
                sample_names.append(dirname);

    # Now we have a list of files to access
    result = pd.DataFrame();
    for sample_name, file_name in zip(sample_names, target_files):
        target_data = pd.read_table(file_name, header=0, index_col=0)
        target_col = target_data[column_name]
        target_col.name = sample_name
        result = result.join(target_col, how='outer')

    result.to_csv(output_file_name, sep='\t')

def gatherQC(path_to_target, output_file_name):
    # Get all target_files
    target_files = []
    sample_names = []
    for dirname in os.listdir(os.getcwd()):
        if os.path.isdir(dirname):
            target_file = os.path.join(dirname, path_to_target)
            if os.path.isfile(target_file):
                target_files.append(target_file);
                sample_names.append(dirname);

    # Now we have a list of files to access
    result = pd.DataFrame();
    for sample_name, file_name in zip(sample_names, target_files):
        qc_data = pd.read_table(file_name, index_col=0, header=None)
        qc_data.columns = [sample_name]
        result = result.join(qc_data, how='outer')

    result.to_csv(output_file_name, sep='\t')


gatherResult("RSEM_Out/results.genes.results", "TPM", "TPM_Matrix.txt")
gatherResult("RSEM_Out/results.genes.results", "expected_count", "Count_Matrix.txt")
gatherQC("RSEM_Out/QC.txt", "QC_all.txt")
