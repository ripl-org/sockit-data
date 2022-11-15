import json
import os
import pandas as pd
import requests

url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
headers = {"Content-Type": "application/json"}
data = {
    "startyear": "2019", 
    "endyear":"2021",
    "registrationkey": os.environ["BLS_API_KEY"]
}

for series in open("series.txt"):

    series = series.strip()
    print(series)

    data["seriesid"] = [series]
    response = requests.post(url, headers=headers, json=data).json()

    with open(f"{series}.json", "w") as f:
        f.write(json.dumps(response))

    if "series" in response["Results"]:
        pd.DataFrame().from_records(response["Results"]["series"][0]["data"]).to_csv(f"{series}.csv", index=False)
