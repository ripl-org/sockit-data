import pandas as pd
import sys

filtered_file = sys.argv[1]
batch_files   = sys.argv[2:]

titles = pd.read_csv(filtered_file, usecols=["truncated_title"]).rename(columns={"truncated_title": "JobTitle"})
titles["SIC"] = ""
titles["JobTask"] = ""

batch = 500000

for i in range(0, len(titles), batch):
    print(f"SOCcer batch {i}")
    titles.iloc[i:i+batch].to_csv(batch_files[int(i/batch)], index=False)
