import pandas as pd
columns = ["year", "month", "state", "jolts"]
jolts = pd.DataFrame(columns=columns)
fips = pd.read_csv("fips.csv", dtype=str)
for row in fips.itertuples():
    jolt = pd.read_csv(f"JTU000000{row.fips}0000000JOL.csv", dtype=str)
    jolt["month"] = jolt["period"].str[1:3]
    jolt["state"] = row.abbr
    jolt["jolts"] = jolt["value"].astype(int) * 1000
    jolts = pd.concat([jolts, jolt[columns]], ignore_index=True)
jolts.to_csv("../openings.csv", index=False)
