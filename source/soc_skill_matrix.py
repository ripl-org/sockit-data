import numpy as np
import pandas as pd
import sys
from scipy.sparse import load_npz
from sklearn.feature_extraction.text import TfidfTransformer

(
    soc2018_file,
    skills_file,
    soc_job_file,
    job_skill_file,
    idf_file,
    soc_skill_file,
    soc_skill_csv_file
) = sys.argv[1:]

N_THRESHOLD = 30

soc2018 = pd.read_csv(soc2018_file, usecols=["soc"], dtype=str).soc
skills = pd.read_csv(skills_file).skill

# Load job matrices

soc_job = load_npz(soc_job_file)
job_skill = load_npz(job_skill_file)

# TF-IDF on job skill matrix

tfidf = TfidfTransformer()
tfidf.fit(job_skill)
np.savetxt(idf_file, tfidf.idf_, fmt="%.3f")
job_skill = tfidf.transform(job_skill, copy=False)

# SOC skill matrix

soc_skill = pd.DataFrame((soc_job * job_skill).todense())
soc_skill["count"] = soc_skill.sum(axis=1)
soc_skill["soc2018"] = soc2018
soc_skill.set_index("soc2018", inplace=True)
fill_rows = soc_skill["count"] <= N_THRESHOLD

# Fill missing rows with 4-digit SOC values

soc4_skill = soc_skill.copy()
soc4 = soc4_skill.index.str[:4]
for col in soc4_skill.columns:
    soc4_skill[col] = soc4_skill[col].groupby(soc4).transform("sum")
for col in soc4_skill.columns[:-1]:
    soc4_skill[col] /= soc4_skill["count"]
del soc4_skill["count"]

for col in soc_skill.columns[:-1]:
    soc_skill[col] /= soc_skill["count"]
del soc_skill["count"]
soc_skill.loc[fill_rows,:] = soc4_skill.loc[fill_rows,:]

# Normalize and save matrix
soc_skill = soc_skill.to_numpy(dtype=float)
soc_skill *= 1.0 / np.sum(soc_skill, axis=1).reshape((soc_skill.shape[0], 1))
np.savetxt(soc_skill_file, soc_skill * 1e6, fmt="%.0f")
pd.DataFrame(soc_skill, index=soc2018, columns=skills).to_csv(soc_skill_csv_file)
