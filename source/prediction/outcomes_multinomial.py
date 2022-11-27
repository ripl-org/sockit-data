import numpy as np
import pandas as pd
import sys
from scipy import sparse

soc_file, soc_job_file, out_file = sys.argv[1:]

socs = pd.read_csv(soc_file)

soc_job = sparse.load_npz(soc_job_file)

# Transpose SOC-job matrix and transform to indicators.
outcomes = (
	pd
	.DataFrame({"soc_id": np.asarray(soc_job.T.argmax(axis=1)).flatten()})
	.merge(socs, on="soc_id", how="left")
)

# Save sparse outcomes matrix
np.save(out_file, outcomes.soc.astype(str).str[:4])
