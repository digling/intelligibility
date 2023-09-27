from lingpy import *
from collections import defaultdict
from csvw.dsv import UnicodeReader
from lingpy.sequence.sound_classes import sampa2uni

# load celect-german to get a lookup for segmented forms
german_lookup = {}
for row in csv2list("raw/celex-german.tsv", strip_lines=False)[1:]:
    german_lookup[row[0]] = (
            row[1], 
            " ".join(tokens2class(row[1].split(), "dolgo"))
            )
    german_lookup[row[0].lower] = german_lookup[row[0]]
# dutch lookup
dutch_lookup = {}
for row in csv2list("raw/celex-dutch.tsv", strip_lines=False)[1:]:
    dutch_lookup[row[0]] = (
            row[1], 
            " ".join(tokens2class(row[1].split(), "dolgo"))
            )

# load cognates to compare against the lrs data
etyma_dutch, etyma_german = {}, {}
cognates = {}
for row in csv2list("data/etyma.tsv", strip_lines=False)[1:]:
    etyma_dutch[row[1]] = (row[3], row[5], row[6])
    etyma_german[row[0]] = (row[2], row[4], row[6])
    cognates[row[6]] = (row[1], row[0])

# load the data
table = [[
    "German_Headword",
    "Dutch_Headword",
    "German_IPA",
    "Dutch_IPA",
    "German_Sound_Classes",
    "Dutch_Sound_Classes",
    "LSR_ID",
    "Cognateset_ID"
    ]]
for row in csv2list("raw/lrsdatabase.tsv", strip_lines=False)[1:]:
    dutch = row[4]
    german = row[5]
    cogid_dutch = row[9].strip()
    cogid_german = row[10].strip()
    if cogid_dutch and cogid_german and cogid_dutch == cogid_german:
        cogid = ""
        if dutch in etyma_dutch:
            cogid = etyma_dutch[dutch][-1]
        elif german in etyma_german:
            cogid = etyma_german[german][-1]

        # try get reading from celex
        dutch_ipa, dutch_cls = dutch_lookup.get(dutch, ["", ""])
        german_ipa, german_cls = german_lookup.get(german, ["", ""])


        table += [[
            german,
            dutch,
            " ".join(ipa2tokens(sampa2uni(row[12]))),
            " ".join(ipa2tokens(sampa2uni(row[11]))),
            " ".join(tokens2class(ipa2tokens(sampa2uni(row[12])), "dolgo")),
            " ".join(tokens2class(ipa2tokens(sampa2uni(row[11])), "dolgo")),
            row[3],
            cogid]]

with open("data/lsr.tsv", "w") as f:
    for row in table:
        f.write("\t".join(row)+"\n")
