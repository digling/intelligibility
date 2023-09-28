from lingpy import *

for lng in ["dutch", "german"]:
    data = csv2list("raw/celex-{0}.tsv".format(lng), strip_lines=False)
    table = [[
        "HEADWORD",
        "IPA",
        "SOUND_CLASSES"
        ]]
    for row in data[1:]:
        table += [[row[0], row[1], " ".join(tokens2class(row[1].split(), "dolgo"))]]
    with open("data/"+lng+"-celex.tsv", "w") as f:
        for row in table:
            f.write("\t".join(row)+"\n")
