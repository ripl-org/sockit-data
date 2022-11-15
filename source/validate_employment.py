import pandas as pd
import sys

nlx_file, employment_file, out_file = sys.argv[1:]

nlx = pd.read_csv(nlx_file, dtype=str)
nlx["soc2"] = nlx["soc"].str[:2]
nlx["freq"] = nlx["freq"].astype(float)
nlx = (
    nlx
    .groupby(["soc2", "year"])
    .agg({"freq": "sum"})
    .reset_index()
    .rename(columns={"freq": "nlx"})
)
nlx["nlx"] = nlx["nlx"].astype(int)

employment = pd.read_csv(employment_file, dtype=str)
employment = employment[employment["soc2"].notnull()]
employment["acs_label"] = employment["acs_label"].str.replace(" occupations", "").str.rstrip(":")
employment = (
    pd.wide_to_long(
        employment,
        stubnames=["acs_all_", "acs_fulltime_", "oes_"],
        i=["soc2", "acs_label"],
        j="year"
    )
    .reset_index()
    .astype(str)
    .merge(nlx, how="left", on=["soc2", "year"])    
)

employment.columns = [x.strip("_") for x in employment.columns]
employment.to_csv(out_file, index=False)
