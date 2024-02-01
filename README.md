# Data and Code Accompanying the Study "A Computational Model for the Assessment of Mutual Intelligibility Among Closely Related Languages" by Nieder and List from 2024

This repository provides data and source code for the following study:

> Nieder, J. and List, J.-M. (2024): A Computational Model for the Assessment of Mutual Intelligibility Among Closely Related Languages. In: Proceedings of the 6th Workshop on Research in Computational Linguistic Typology and Multilingual NLP (SIGTYP 2024).

## Installation

In order to run the scripts provided here, you must have Python (Version 3.8 or higher) and Julia (Version 1.10 or higher).

To run the Python script, make first sure to create a new virtual environment and then install all dependencies typing:

```
pip install -r requirements.txt
```

## Running the Scripts

All scripts provided in this directory should be run in the order in which they are numbered, starting from the Python script.

To run this, simply type:

```
python cosinesimilarity_etyma.py
```

To run the remaining Julia script, start them from the commandline and point to the `config` folder as the folder with the project information:

```
julia --project=config LDL_etyma_2-grams.jl
```

## Running the Preprocessing Steps

To test the preprocessing steps we used to get the data into the form used here, please turn to the [`preprocessing/README.md`](preprocessing/README.md) file that provides more information.
