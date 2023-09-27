from lingpy import *

wl = Wordlist("raw/germanic.tsv")
table = [[
        "German_Headword",
        "Dutch_Headword",
        "German_IPA",
        "Dutch_IPA",
        "German_Sound_Classes",
        "Dutch_Sound_Classes",
        "Cognateset_ID"
        ]]
etd = wl.get_etymdict(ref="cogid")
for cogid, vals in etd.items():
    idxs = []
    for idx in vals:
        if idx:
            idxs += [idx[0]]
    languages = [wl[idx, "doculect"] for idx in idxs]
    if "Dutch" in languages and "German" in languages:
        idx_german = idxs[languages.index("German")]
        idx_dutch = idxs[languages.index("Dutch")]
        table += [[
            wl[idx_german, "counterpart"],
            wl[idx_dutch, "counterpart"],
            " ".join(wl[idx_german, "tokens"]),
            " ".join(wl[idx_dutch, "tokens"]),
            " ".join(tokens2class(wl[idx_german, "tokens"], "dolgo")),
            " ".join(tokens2class(wl[idx_dutch, "tokens"], "dolgo")),
            str(cogid)]]
with open("data/etyma.tsv", "w") as f:
    for row in table:
        f.write("\t".join(row)+"\n")
