from lingpy import *
from lingpy.evaluate.acd import _get_bcubed_score as bcube
from tabulate import tabulate
from itertools import combinations
from lingpy.sequence.ngrams import bigrams

wl = Wordlist("raw/germanic.tsv")

# get cognates for all pairs
etd = wl.get_etymdict(ref="cogid")

# we compute b-cubed scores
alms_g, alms_d, alms_e = [], [], []
for cogid, idxs_ in etd.items():
    idxs = []
    for idx in idxs_:
        if idx:
            idxs += [idx[0]]
    taxa = [wl[idx, 'doculect'] for idx in idxs]
    if "German" in taxa and "English" in taxa and "Dutch" in taxa:
        idx_g, idx_d, idx_e = (
                idxs[taxa.index('German')],
                idxs[taxa.index('Dutch')],
                idxs[taxa.index('English')])
        alm_g, alm_d, alm_e = (
                wl[idx_g, "alignment"],
                wl[idx_d, "alignment"],
                wl[idx_e, "alignment"])
        for a, b, c in zip(bigrams(alm_g), bigrams(alm_d), bigrams(alm_e)):
            alms_g += [a]
            alms_d += [b]
            alms_e += [c]

table = [["Language 1", "Language 2", "Score"]]
for (a_1, b_1), (a_2, b_2) in combinations(
        [("German", alms_g), ("Dutch", alms_d), ("English", alms_e)], r=2):
    table += [[a_1, a_2, bcube(b_1, b_2)]]
    table += [[a_2, a_1, bcube(b_2, b_1)]]
print(tabulate(table, tablefmt="pipe"))

