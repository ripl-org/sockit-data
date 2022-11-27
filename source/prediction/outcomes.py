import pandas as pd
import sys
from scipy import sparse

soc2018_file, soc_job_file, counts_file, out_file = sys.argv[1:]

socs    = pd.read_csv(soc2018_file, dtype=str)
soc_job = sparse.load_npz(soc_job_file)

# Transpose SOC-job matrix and transform to indicators.
outcomes = (100*soc_job.T).minimum(1)

# Count outcomes by SOC
counts = pd.DataFrame(
    {"count": outcomes.sum(axis=0).tolist()[0]},
    index=socs.soc
)
counts.index.name = "soc"
print(counts)
counts.to_csv(counts_file)

# Save sparse outcomes matrix
sparse.save_npz(out_file, outcomes)
