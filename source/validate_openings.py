import pandas as pd
import sys

nlx_file, openings_file, out_file = sys.argv[1:4]

nlx = pd.read_csv(nlx_file, dtype=str)
nlx["nlx"] = nlx["freq"].astype(float)
nlx = nlx.groupby(["year", "month", "state"]).agg({"nlx": "sum"}).reset_index()
nlx["nlx"] = nlx["nlx"].astype(int)

(
    pd.read_csv(openings_file, dtype=str)
    .merge(nlx, how="left", on=["year", "month", "state"])
    .to_csv(out_file, index=False)
)
