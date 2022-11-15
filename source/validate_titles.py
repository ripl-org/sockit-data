import pandas as pd
from sockit.title import clean, search, sort
import sys

socs_file, titles_file, top, out_file = sys.argv[1:]

top = int(top)

titles = pd.read_csv(titles_file, sep="\t", dtype=str, usecols=[0, 1])
titles.columns = ["soc", "title"]
titles["soc"] = titles["soc"].str[:2] + titles["soc"].str[3:7]

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
    print("title", "soc", "match6", "match5", "match3", "match2", sep=",", file=f)
    for row in titles.itertuples():
        socs = sort(search(clean(row.title)))
        print(f"\"{row.title}\"", row.soc, *matches(row.soc, socs), sep=",", file=f)
