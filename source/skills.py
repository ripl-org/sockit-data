import csv
import sys
from wordtrie import WordTrie

skills_file1, skills_file2, trie_file, csv_file = sys.argv[1:]

skills = set()
trie = WordTrie()

with open(skills_file1) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["final"] != "x":
            skills.add(row["final"])
            trie.add(row["original"], row["final"])

with open(skills_file2) as f:
    reader = csv.DictReader(f)
    for row in reader:
        skills.add(row["skill"])
        trie.add(row["ngram"], row["skill"])

trie.to_json(trie_file)

with open(csv_file, "w", newline="\n") as f:
    writer = csv.writer(f)
    writer.writerow(("skill_id", "skill"))
    for i, skill in enumerate(sorted(skills, key=lambda x: x.lower().replace("-", ""))):
        writer.writerow((str(i), skill))
