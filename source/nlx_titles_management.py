import pandas as pd
import re
import sys
from numpy import nan
from wordtrie import WordTrie

(
    titles_file,
    nlx_companies_file,
    us_places_file,
    schedule_terms_file,
    out_titles_file,
    out_words_file
) = sys.argv[1:]

managers = ["manager", "director", "supervisor", "vp", "president"]

re_punct     = re.compile(r"[\-+/|]")
re_alphanum  = re.compile(r"[^a-z0-9 \.]+")
re_manager   = re.compile("|".join(managers))

def clean(text):
    """
    Convert some puncuation to spaces, and return alpha-numeric
    characters, spaces and periods.
    """
    return re_alphanum.sub("", re_punct.sub(" ", text.lower())).strip()

def is_manager(title):
	if title is not nan and title:
		return re_manager.search(title) is not None
	else:
		return False

trie_filter = WordTrie()

for line in open(nlx_companies_file):
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
for stopword in managers + ["associate", "assistant", "senior", "junior", "deputy", "vice"]:
    trie_filter.add(stopword, stopword)

def filter_words(title):
    title = str(title)
    for match in trie_filter.search(title, return_nodes=True):
        title = title.replace(" ".join(match[0]), "")
    return " ".join(word for word in title.split() if len(word) > 3)

titles = pd.read_csv(titles_file)
titles = titles[titles["clean_title"].apply(is_manager)]
titles["clean_title"] = titles["clean_title"].apply(filter_words)
titles = titles[titles["clean_title"] != ""].groupby("clean_title").agg({"n": "sum"})
titles.sort_values("n", ascending=False).to_csv(out_titles_file)

words = {}
for title, row in titles.iterrows():
	for word in title.split():
		words[word] = words.get(word, 0) + 1
words = pd.DataFrame({"word": words.keys(), "n": words.values()})
words.sort_values("n", ascending=False).to_csv(out_words_file, index=False)
