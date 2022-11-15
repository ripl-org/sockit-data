import json
import pandas as pd
import sys

infile, outfile = sys.argv[1:]

acronyms = pd.read_csv(infile, usecols=["acronym", "soc"])
acronyms["soc"] = acronyms["soc"].apply(lambda x: x.replace("-", "")[:6])

# Keep acronyms that map directly to a SOC
acronyms = acronyms.drop_duplicates().drop_duplicates("acronym", keep=False)
acronyms = dict((row.acronym, row.soc) for row in acronyms.itertuples())

# Remove abiguities
acronyms.pop("cat") # Ambiguous with CAT scans
acronyms.pop("mc") # Ambiguous with "Medical Center"

# Write lookup table
with open(outfile, "w") as f:
    json.dump(acronyms, f, indent=2)
