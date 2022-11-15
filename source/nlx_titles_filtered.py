import pandas as pd
import re
import sys
from wordtrie import WordTrie

(
    titles_file,
    nlx_company_file,
    us_places_file,
    schedule_terms_file,
    nouns_file,
    out_file,
) = sys.argv[1:]

re_punct     = re.compile(r"[\-+/|]")
re_alphanum  = re.compile(r"[^a-z0-9 \.]+")

def clean(text):
    """
    Convert some puncuation to spaces, and return alpha-numeric
    characters, spaces and periods.
    """
    return re_alphanum.sub("", re_punct.sub(" ", text.lower())).strip()

print("Loading titles")

titles = pd.read_csv(titles_file)

print("Found", len(titles), "titles, totalling", titles["n"].sum(), "job postings")

print(f"Filtering company names, places and schedule words form titles")

trie_filter = WordTrie()
for line in open(nlx_company_file):
    name = line.strip()
    if name:
        trie_filter.add(clean(name), name)
for line in open(us_places_file):
    name = line.strip()
    if name:
        trie_filter.add(clean(name), name)
for line in open(schedule_terms_file):
    name = line.strip()
    if name:
        trie_filter.add(clean(name), name)

def filter_words(title):
    title = str(title)
    for match in trie_filter.search(title, return_nodes=True):
        title = title.replace(" ".join(match[0]), "")
    return title

titles["filtered_title"] = titles["clean_title"].apply(filter_words)
filtered = titles["clean_title"] != titles["filtered_title"]
n = titles.loc[filtered, "n"].sum()

print("Filtered words from", sum(filtered), "titles, totalling", n, "job postings")

print("Reordering titles")

def reorder(title):
    """
    Reorder titles around prepositional phrases so that the principal
    noun ends the title, e.g.:
    "Director of Reseach" to "Research Director"
    "Teacher for Special Needs" to "Special Needs Teacher"
    "Assistant to the CEO" to "the CEO assistant"
    """
    suffix, _, prefix = title.partition(" or ")
    title = f"{prefix} {suffix}".strip()
    suffix, _, prefix = title.partition(" for ")
    title = f"{prefix} {suffix}".strip()
    suffix, _, prefix = title.partition(" to ")
    title = f"{prefix} {suffix}".strip()
    return title

titles["reordered_title"] = titles["filtered_title"].apply(reorder)
reordered = titles["filtered_title"] != titles["reordered_title"]
n = titles.loc[reordered, "n"].sum()

print("Reordered", sum(reordered), "titles, totalling", n, "job postings")

print("Finding nouns")

nouns = set(noun.strip() for noun in open(nouns_file))

def find_noun(title):
    words = title.split()
    if words:
        for i in range(len(words), 0, -1):
            if words[i-1] in nouns:
                break
        if i > 1 or words[0] in nouns:
            return " ".join(words[:i])
    else:
        return ""

titles["noun_title"] = titles["reordered_title"].apply(find_noun).fillna("")
has_noun = titles["noun_title"] != ""
n = titles.loc[has_noun, "n"].sum()

print("Found noun in", sum(has_noun), "titles, totalling", n, "job postings")

print("Truncating to three words or less")

titles = titles[has_noun]

def truncate(title):
    words = [word for word in title.split() if len(word) > 2]
    return " ".join(words[-3:])

titles["truncated_title"] = titles["noun_title"].apply(truncate)
truncated = titles["noun_title"] != titles["truncated_title"]
n = titles.loc[truncated, "n"].sum()

print("Truncated", sum(truncated), "titles, totalling", n, "job postings")

print("Grouping titles")

titles = titles[titles["truncated_title"] != ""].groupby("truncated_title").agg({"n": "sum"})

print("Grouped", len(titles), "titles, totalling", titles["n"].sum(), "job postngs")

titles.sort_values("n", ascending=False).to_csv(out_file)
