download-numberbatch:
	curl -o "numberbatch.txt.gz" "https://conceptnet.s3.amazonaws.com/downloads/2019/numberbatch/numberbatch-19.08.txt.gz"
	gunzip "numberbatch.txt.gz"

download-germancognates:
	git clone https://github.com/lexibank/germancognates.git
	cd germancognates; git checkout v0.1

install-python:
	pip install -r requirements.txt

prepare-words:
	edictor wordlist --data=germancognates/cldf/cldf-metadata.json --addon="cognacy:cogid,alignment:alignment" --name="germancognates"
	python prepare-etyma-full.py
	python prepare-etyma-trimmed.py

prepare-vectors:
	python extract-vectors.py
	python prepare-vectors.py
	python prepare-vectors-trimmed.py


