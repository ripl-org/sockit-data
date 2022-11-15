import csv
import json
import pandas as pd
import sockit.data
from collections import defaultdict
from wordtrie import WordTrie
import sys

(
    managers_file,
    crosswalk_file,
    filtered_file,
    soccer_file1,
    soccer_file2,
    handcoded_file,
    trie_file,
    override_file,
) = sys.argv[1:]

SOCCER_THRESHOLD = 0.02

# Load the SOC 2010 to 2018 crosswalk.
crosswalk = defaultdict(list)
for row in csv.DictReader(open(crosswalk_file)):
    crosswalk[row["2010 SOC Code"]].append(row["2018 SOC Code"])

# Load the title counts from the filtered titles file.
counts = {}
for row in csv.DictReader(open(filtered_file)):
    counts[row["truncated_title"]] = float(row["n"])

# Manager titles
managers_trie = WordTrie()
with open(managers_file) as f:
    for title, socs in json.load(f).items():
        nodes = title.split()[::-1] # Insert titles in reverse order so that principal noun is first
        managers_trie.add(nodes, {soc.replace("-", ""): 1 for soc in socs})

# Process the SOCcer results.
trie = WordTrie()
titles = []
for filename in [soccer_file1, soccer_file2]:
    for row in csv.DictReader(open(filename)):
        value = {}
        n = counts[row["JobTitle"]]
        # SOCcer reports the top 10 matches with probability scores.
        for i in range(1, 11):
            score = float(row[f"Score_{i}"])
            # Keep only the matches above the score threshold.
            if score > SOCCER_THRESHOLD:
                # Scale the counts by the probability score.
                score = int(score * n)
                if score:
                    # Map the SOC 2010 codes from SOCcer to SOC 2018 codes.
                    for soc in crosswalk[row[f"soc2010_{i}"]]:
                        value[soc.replace("-", "")] = score
        if value:
            # If the title has a partial match to a manager title,
            # restrict the results to the same 2-digit SOC code as the
            # matching manager title.
            managers = managers_trie.search(row["JobTitle"])
            if len(managers):
                soc2 = frozenset((soc[:2] for soc in managers[0].keys()))
                value = {soc: n for soc, n in value.items() if soc[:2] in soc2}
            if value:
                titles.append(row["JobTitle"])
                nodes = row["JobTitle"].split()[::-1] # Insert titles in reverse order so that principal noun is first 
                trie.add(nodes, value)

# Roll tips up to parent nodes using an aggregator function.

def _aggregate(old, new):
    """
    Aggregate two dictionaries of SOC/value items.
    """
    value = {}
    for soc in new:
        value[soc] = new[soc] + old.get(soc, 0)
    for soc in old:
        if soc not in value:
            value[soc] = old[soc]
    return value

for title in sorted(titles, key=len, reverse=True):
    nodes = title.split()[::-1]
    value = trie.match(nodes)
    if len(nodes) > 1:
        parent = nodes[:-1]
        trie.add(parent, value, aggregator=_aggregate)

# Add handcoded titles to manager titles to create the override trie.
for row in csv.DictReader(open(handcoded_file)):
    title_test = sockit.data.get_soc_title(row["soc"])
    nodes = row["title"].split()[::-1] # Insert titles in reverse order so that principal noun is first
    managers_trie.add(nodes, {row["soc"]: 1})

# Write output.
trie.to_json(trie_file)
managers_trie.to_json(override_file)
