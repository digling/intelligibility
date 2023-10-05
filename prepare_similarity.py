import pandas as pd
import numpy as np

#### Check semantic similarity of numberbatch vectors for the comparative-wordlist.tsv data
# ATTENTION: this script requires to run 1) download_numberbatch.sh and 2) prepare_numberbatch.py first to create the necessary txt files
# txt files are too large to uploaded to git

# Read in numberbatch data
dutchvectors_numberbatch = pd.read_csv('dutchvectors_numberbatch.tsv',   delimiter="\s", engine='python')
print(dutchvectors_numberbatch)

#germanvectors need to be read in in chunks due to the size and long processing time:
# Define the file path and specifiy the delimiter used in your file
file_path = 'germanvectors_numberbatch.tsv'
delimiter = "\s"  

# Create an empty list for storing chunks
chunks = []

# Define the chunk size 
chunk_size = 1000 

# Read the data in chunks and append them to the created list
for chunk in pd.read_csv(file_path, delimiter=delimiter, engine='python', chunksize=chunk_size):
    chunks.append(chunk)

# Concatenate the list of chunks into a single DataFrame
germanvectors_numberbatch = pd.concat(chunks, axis=0, ignore_index=True)

#### numberbatch data is ready

# Now I will merge the numberbatch data with comparative-wordlist.tsv

# Take string in column 'V1' and only keep the relevant part (= the word form)
germanvectors_numberbatch['V1'] = germanvectors_numberbatch['V1'].str.replace("^.*/", "")
dutchvectors_numberbatch['V1'] = dutchvectors_numberbatch['V1'].str.replace("^.*/", "")

# read in data to merge with:
comparative_data = pd.read_csv('/data/comparative-wordlist.tsv',   delimiter="\t", engine='python')

# I take the Dutch words and German words out of it to merge separately to create two data sets with their vectors
comparative_data_german = comparative_data[['German_Entry']]
comparative_data_german['German_Entry'] = comparative_data_german['German_Entry'] .str.lower() #numberbatch doesn't have capital letters for German nouns, I will change to lowercase
comparative_data_dutch = comparative_data[['Dutch_Entry']]

# Rename the column for the merging process
germanvectors_numberbatch.rename(columns={"V1": "German_Entry"}, inplace=True)
dutchvectors_numberbatch.rename(columns={"V1" : "Dutch_Entry"}, inplace=True)

# replace ß with ss for German data
columns_to_process = ['German_Entry']

# Replace 'ß' with 'ss' in specified columns since otherwise merging creates NAs
for col in columns_to_process:
    comparative_data_german[col] = comparative_data_german[col].str.replace('ß', 'ss')

# Replace # in row 625 win#gerd of the Dutch data to avoid NAs
row_index = 625  # Index of the row with 'win#gerd'
column_name = 'Dutch_Entry'  # Name of the column to modify
if '#' in comparative_data_dutch.at[row_index, column_name]:
   comparative_data_dutch.at[row_index, column_name] = comparative_data_dutch.at[row_index, column_name].replace('#', '')

# Merge data
mergcomparative_data_german = pd.merge(comparative_data_german, germanvectors_numberbatch, on="German_Entry", how="left")
mergcomparative_data_dutch = pd.merge(comparative_data_dutch, dutchvectors_numberbatch, on="Dutch_Entry", how="left")

# Check the number of rows: In total I have 682
num_rows1 = len(mergcomparative_data_german)
print("Number of rows in German data:", num_rows1) 

num_rows2 = len(mergcomparative_data_dutch)
print("Number of rows in Dutch data:", num_rows2) 

# I need to check for potential missing vectors and delete rows to have word pairs again
# Dutch
rows_with_nan_dutch = mergcomparative_data_dutch[mergcomparative_data_dutch.isna().any(axis=1)]
print(rows_with_nan_dutch)

#German
rows_with_nan_german = mergcomparative_data_german[mergcomparative_data_german.isna().any(axis=1)]
print(rows_with_nan_german)

# export the merged DataFrames
mergcomparative_data_german.to_csv('/data/comparative_germandata.csv', index=False)
mergcomparative_data_dutch.to_csv('/data/comparative_dutchdata.csv', index=False)
