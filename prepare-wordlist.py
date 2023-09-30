from lingpy import *

wl = Wordlist("raw/samplesize.tsv")

table = [[
    "Concept",
    "Dutch_Entry",
    "German_Entry",
    "Dutch_Tokens",
    "German_Tokens",
    "Dutch_Sound_Classes",
    "German_Sound_Classes",
    "Cognacy"
    ]]
for concept, dct in wl._dict.items():
    dutch, german = dct["dutch"], dct["german"]
    if dutch and german:
        for idx_a in dutch:
            for idx_b in german:
                table += [[
                    concept,
                    wl[idx_a, "value"],
                    wl[idx_b, "value"],
                    " ".join(wl[idx_a, "tokens"]),
                    " ".join(wl[idx_b, "tokens"]),
                    " ".join(tokens2class(wl[idx_a, "tokens"], "dolgo")),
                    " ".join(tokens2class(wl[idx_b, "tokens"], "dolgo")),
                    "1" if wl[idx_a, "cogid"] == wl[idx_b, "cogid"] else "0"
                    ]]

with open("data/comparative-wordlist.tsv", "w") as f:
    for row in table:
        f.write("\t".join(row)+"\n")
