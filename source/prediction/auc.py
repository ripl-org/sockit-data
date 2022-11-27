import os
import pandas as pd
import re
import sys

soc_file, out_file = sys.argv[1:]

socs = pd.read_csv(soc_file).soc.tolist()

n_pattern         = re.compile(r"Number of positive: (\d+)")
valid_auc_pattern = re.compile(r"valid_0's auc: ([\d\.]+)")
test_auc_pattern  = re.compile(r"Test AUC: ([\d\.]+)")

def extract(lines, pattern):
    for line in lines:
        match = pattern.search(line)
        if match is not None:
            return match.group(1)
    return ""

with open(out_file, "w") as f:
    print("soc,n,valid_auc,test_auc", file=f)
    for soc in socs:
        log_file = f"scratch/prediction/models/{soc}.txt.log"
        n = valid_auc = test_auc = ""
        if os.path.exists(log_file):
            with open(log_file) as log:
                lines = log.readlines()
                n = extract(lines, n_pattern)
                valid_auc = extract(lines, valid_auc_pattern)
                test_auc = extract(lines, test_auc_pattern)
        print(soc, n, valid_auc, test_auc, sep=",", file=f)
