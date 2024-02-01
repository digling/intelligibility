from lingpy import *
from lingpy.evaluate.acd import _get_bcubed_score as bcube
from tabulate import tabulate
from itertools import combinations
from lingpy.sequence.ngrams import bigrams
from lingrex.trimming import Sites
from lingpy.align.sca import reduce_alignment


wl = Wordlist("germancognates.tsv")

grams = lambda x: bigrams(x) # [y for y in tokens2class(x, "dolgo")]

# get cognates for all pairs
etd = wl.get_etymdict(ref="cogid")

# we compute b-cubed scores
alms_g, alms_d, alms_e = [], [], []
gaps = [0, 0, 0]
out = [[
        "German_Headword",
        "Dutch_Headword",
        "English_Headword",
        "German_IPA",
        "Dutch_IPA",
        "English_IPA",
        "German_Sound_Classes",
        "Dutch_Sound_Classes",
        "English_Sound_Classes",
        "Cognateset_ID"
        ]]

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
        alm_g, alm_d, alm_e = reduce_alignment([
                wl[idx_g, "alignment"],
                wl[idx_d, "alignment"],
                wl[idx_e, "alignment"]])
        # trim alignment
        alm_g, alm_d, alm_e = Sites([alm_g, alm_d, alm_e]).trimmed().to_alignment()
        for x in [alm_g, alm_d, alm_e]:
            print("\t".join(x))
        out += [[
            wl[idx_g, "value"],
            wl[idx_d, "value"],
            wl[idx_e, "value"],
            " ".join([x for x in alm_g if x != "-"]),
            " ".join([x for x in alm_d if x != "-"]),
            " ".join([x for x in alm_e if x != "-"]),
            " ".join(tokens2class([x for x in alm_g if x != "-"], "dolgo")),
            " ".join(tokens2class([x for x in alm_d if x != "-"], "dolgo")),
            " ".join(tokens2class([x for x in alm_e if x != "-"], "dolgo")),
            str(cogid)]]
        #input()
        gaps[0] += alm_g.count("-")
        gaps[1] += alm_d.count("-")
        gaps[2] += alm_e.count("-")
        for a, b, c in zip(grams(alm_g), grams(alm_d), grams(alm_e)):
            alms_g += [a]
            alms_d += [b]
            alms_e += [c]

table = [["Language 1", "Language 2", "Score"]]
for (a_1, b_1), (a_2, b_2) in combinations(
        [("German", alms_g), ("Dutch", alms_d), ("English", alms_e)], r=2):
    table += [[a_1, a_2, bcube(b_1, b_2)]]
    table += [[a_2, a_1, bcube(b_2, b_1)]]
print("# Prediction (B-Cubes, Bigrams, Trimmed)")
print(tabulate(table, tablefmt="pipe", headers="firstrow"))
print("# Gaps (trimmed)")
print(tabulate([gaps], headers=["German", "Dutch", "English"], tablefmt="pipe"))

with open('etyma-trimmed.tsv', "w") as f:
    for row in out:
        f.write("\t".join(row)+"\n")
