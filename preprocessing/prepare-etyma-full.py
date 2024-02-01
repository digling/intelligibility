from lingpy import *

wl = Wordlist("germancognates.tsv")
table = [[
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
etd = wl.get_etymdict(ref="cogid")
for cogid, vals in etd.items():
    idxs = []
    for idx in vals:
        if idx:
            idxs += [idx[0]]
    languages = [wl[idx, "doculect"] for idx in idxs]
    if "Dutch" in languages and "German" in languages and "English" in languages:
        idx_german = idxs[languages.index("German")]
        idx_dutch = idxs[languages.index("Dutch")]
        idx_english = idxs[languages.index("English")]
        table += [[
            wl[idx_german, "value"],
            wl[idx_dutch, "value"],
            wl[idx_english, "value"],
            " ".join(wl[idx_german, "tokens"]),
            " ".join(wl[idx_dutch, "tokens"]),
            " ".join(wl[idx_english, "tokens"]),
            " ".join(tokens2class(wl[idx_german, "tokens"], "dolgo")),
            " ".join(tokens2class(wl[idx_dutch, "tokens"], "dolgo")),
            " ".join(tokens2class(wl[idx_english, "tokens"], "dolgo")),
            str(cogid)]]
with open("etyma-full.tsv", "w") as f:
    for row in table:
        f.write("\t".join(row)+"\n")
