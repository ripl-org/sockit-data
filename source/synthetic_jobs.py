import os
import pandas as pd
import sys

socs_file, occ_file, task_file, task_dwa_file, dwa_file, sentinel_file = sys.argv[1:]

outdir    = os.path.dirname(sentinel_file)
socs      = pd.read_csv(socs_file, dtype=str)
desc      = pd.read_csv(occ_file, delimiter="\t", dtype=str, index_col="O*NET-SOC Code")
task      = pd.read_csv(task_file, delimiter="\t", dtype=str)
activity  = task.merge(
                pd.read_csv(task_dwa_file, delimiter="\t", dtype=str, usecols=["Task ID", "DWA ID"]),
                how="left",
                on="Task ID"
            ).merge(
                pd.read_csv(dwa_file, delimiter="\t", dtype=str, usecols=["DWA ID", "DWA Title"]),
                how="left",
                on="DWA ID"
            ).dropna()

checksum = 0
for soc in socs.soc:
    soc = "{}-{}.00".format(soc[:2], soc[2:])
    print("Synthetic job posting", soc)
    with open(f"{outdir}/{soc}.txt", "w") as f:
        posting = "\n".join((
            desc.loc[soc, "Title"],
            desc.loc[soc, "Description"],
            "\n".join(task.loc[task["O*NET-SOC Code"] == soc, "Task"]),
            "\n".join(activity.loc[activity["O*NET-SOC Code"] == soc, "DWA Title"])
        ))
        checksum += hash(posting)
        print(posting, file=f)
        
open(sentinel_file, "w").write(str(checksum))
