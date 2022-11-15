import os
import pandas as pd
import sockit.parse
import sys

socs_file, jobs_file, top, out_file = sys.argv[1:]

socs   = pd.read_csv(socs_file, dtype=str)
jobdir = os.path.dirname(jobs_file)
top    = int(top)

def matches(soc, sockit_list):
    result = [0] * 4
    for s in sockit_list[:top]:
        if s["soc"] == soc:
            result[0] = 1
        if s["soc"][:5] == soc[:5]:
            result[1] = 1
        if s["soc"][:3] == soc[:3]:
            result[2] = 1
        if s["soc"][:2] == soc[:2]:
            result[3] = 1
    return result

with open(out_file, "w") as f:
    print("soc", "match6", "match5", "match3", "match2", sep=",", file=f)
    for soc in socs.soc:
        try:
            parsed = sockit.parse.parse_job_posting(f"{jobdir}/{soc[:2]}-{soc[2:]}.00.txt", "txt")
        except:
            parsed = None
        if parsed:
            print(soc, *matches(soc, parsed["Occupations"]), sep=",", file=f)
