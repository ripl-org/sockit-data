import json
import numpy as np
import pandas as pd
import sockit.data
import sys
from scipy import spatial

soc_skill_file, skills_file, summary_file = sys.argv[1:4]
soc_distance_files = sys.argv[4:]
assert len(soc_distance_files) == 4

soc_skill = pd.read_csv(soc_skill_file, index_col="soc")
index = soc_skill.index

X = soc_skill.to_numpy(dtype=float)
N = X.shape[0]

methods = ["euclidean", "manhattan", "cosine", "kl"]

def kl(p, q):
    return np.sum(p * np.nan_to_num(np.log(p / q), True, 0, 0, 0))

D = np.zeros((len(methods),N,N))
for i in range(N):
    for j in range(i, N):
        D[0,i,j] = D[0,j,i] = spatial.distance.euclidean(X[i,:], X[j,:])
        D[1,i,j] = D[1,j,i] = spatial.distance.cityblock(X[i,:], X[j,:])
        D[2,i,j] = D[2,j,i] = spatial.distance.cosine(X[i,:], X[j,:])
        D[3,i,j] = kl(X[i,:], X[j,:])
        D[3,j,i] = kl(X[j,:], X[i,:])

for i, method in enumerate(methods):
    df = pd.DataFrame(D[i,:,:], index=index)
    df.columns = index.to_list()
    df.to_csv(soc_distance_files[i])

# Turn skill probability columns into Z-scores
for col in soc_skill.columns:
    soc_skill[col] = (soc_skill[col] - soc_skill[col].mean()) / soc_skill[col].std()

skills = pd.read_csv(skills_file, index_col="skill_id").skill.to_dict()
index = [str(soc) for soc in index]
distance = D[1,:,:]

with open(summary_file, "w") as f:
    for i, soc in enumerate(index):
        top_skills = [skills[k] for k in soc_skill.iloc[i].argsort()[-5:]]
        print(soc, sockit.data.get_soc_title(soc), "|", ", ".join(top_skills), file=f)
        for j in distance[i,:].argsort()[1:6]:
            top_skills = [skills[k] for k in soc_skill.iloc[j].argsort()[-5:]]
            print(
                ">",
                "{:.3f}".format(distance[i,j]),
                "|",
                index[j],
                sockit.data.get_soc_title(index[j]),
                "|",
                ", ".join(top_skills),
                file=f
            )
        print("", file=f)
