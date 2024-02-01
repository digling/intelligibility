import pandas as pd
import numpy as np
from pathlib import Path

# ATTENTION: this script requires to run 1) download_numberbatch.sh and 2) prepare_numberbatch.py first to create the necessary txt files
# txt files are relatively large

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

#englishvectors need to be read in in chunks due to the size and long processing time:
# Define the file path and specifiy the delimiter used in your file
file_path = 'englishvectors_numberbatch.tsv'
delimiter = "\s"  

# Create an empty list for storing chunks
chunks = []

# Define the chunk size 
chunk_size = 1000 

# Read the data in chunks and append them to the created list
for chunk in pd.read_csv(file_path, delimiter=delimiter, engine='python', chunksize=chunk_size):
    chunks.append(chunk)

# Concatenate the list of chunks into a single DataFrame
englishvectors_numberbatch = pd.concat(chunks, axis=0, ignore_index=True)
#### numberbatch data is ready

# merge numberbatch data with etyma data

# Take string in column 'V1' and only keep the relevant part (= the word form)
germanvectors_numberbatch['V1'] = germanvectors_numberbatch['V1'].str.split('/').str[-1]
dutchvectors_numberbatch['V1'] = dutchvectors_numberbatch['V1'].str.split('/').str[-1]
englishvectors_numberbatch['V1'] = englishvectors_numberbatch['V1'].str.split('/').str[-1]

# read in data to merge with:
etyma = pd.read_csv('etyma-full.tsv',   delimiter="\t", engine='python')

# take Dutch words and German words out of it to merge separately to create two semantic matrices
etyma_german = etyma[['German_Headword', 'German_IPA', 'German_Sound_Classes']]
etyma_german['German_Headword'] = etyma_german['German_Headword'].str.lower() #numberbatch doesn't have capital letters for German nouns, change to lowercase
etyma_dutch = etyma[['Dutch_Headword', 'Dutch_IPA', 'Dutch_Sound_Classes']]
etyma_english = etyma[['English_Headword', 'English_IPA', 'English_Sound_Classes']]

# Rename the column for the merging process
etyma_german.rename(columns={"German_Headword": "Headword"}, inplace=True)
etyma_dutch.rename(columns={"Dutch_Headword": "Headword"}, inplace=True)
etyma_english.rename(columns={"English_Headword": "Headword"}, inplace=True)

germanvectors_numberbatch.rename(columns={"V1": "Headword"}, inplace=True)
dutchvectors_numberbatch.rename(columns={"V1" : "Headword"}, inplace=True)
englishvectors_numberbatch.rename(columns={"V1" : "Headword"}, inplace=True)

# Merge data
merged_etyma_german = pd.merge(etyma_german, germanvectors_numberbatch, on="Headword", how="left")
merged_etyma_dutch = pd.merge(etyma_dutch, dutchvectors_numberbatch, on="Headword", how="left")
merged_etyma_english = pd.merge(etyma_english, englishvectors_numberbatch, on="Headword", how="left")

# Check the number of rows
num_rows1 = len(merged_etyma_german)
print("Number of rows in German data:", num_rows1)

num_rows2 = len(merged_etyma_dutch)
print("Number of rows in Dutch data:", num_rows2) 

num_rows3 = len(merged_etyma_english)
print("Number of rows in English data:", num_rows3) 

# check for potential missing vectors and delete rows to have word pairs again
# Dutch
rows_with_nan_dutch = merged_etyma_dutch[merged_etyma_dutch.isna().any(axis=1)]
print(rows_with_nan_dutch) #329  beukeboom has no vectors

#German
rows_with_nan_german =merged_etyma_german[merged_etyma_german.isna().any(axis=1)]
print(rows_with_nan_german)

#English
rows_with_nan_english =merged_etyma_english[merged_etyma_english.isna().any(axis=1)]
print(rows_with_nan_english)

# Delete rows with NaN values from mergcomparative_data_dutch
merged_etyma_dutch = merged_etyma_dutch.dropna()

# delete the German and English counterparts of beukeboom from the data to have the same amount of words with their respective counterparts
# Define the row number you want to use as the condition for deletion

# Row number to delete
row_number_to_delete = 329

# Delete the row with the specified row number from the German DataFrame
merged_etyma_german = merged_etyma_german.drop(merged_etyma_german.index[row_number_to_delete])

# Delete the row with the specified row number from the English DataFrame
merged_etyma_english = merged_etyma_english.drop(merged_etyma_english.index[row_number_to_delete])

# save vectors as matrix for LDL
#  Select columns 
columns_to_select = list(range(3, 303))  # Python uses 0-based indexing

# Extract the selected columns as a DataFrame
S_DUT = merged_etyma_dutch.iloc[:, columns_to_select]
S_ENG = merged_etyma_english.iloc[:, columns_to_select]
S_GER = merged_etyma_german.iloc[:, columns_to_select]

# Convert the DataFrame to a numpy matrix
S_DUT_matrix = S_DUT.to_numpy()
S_ENG_matrix = S_ENG.to_numpy()
S_GER_matrix= S_GER.to_numpy()

# Save the numpy matrix to a file
np.save(Path(__file__).parent.parent / "data" / "S_DUT_etymamatrix.npy", S_DUT_matrix)
np.save(Path(__file__).parent.parent / "data" / "S_ENG_etymamatrix.npy", S_ENG_matrix)
np.save(Path(__file__).parent.parent / "data" / "S_GER_etymamatrix.npy", S_GER_matrix)

# Save dutch and german data without vectors separately 
etyma_germandata = merged_etyma_german[['Headword', 'German_IPA', 'German_Sound_Classes']]
etyma_germandata.to_csv(
        Path(__file__).parent.parent / "data" / 'etyma_germandata.tsv', sep='\t', index=False)

etyma_englishdata = merged_etyma_english[['Headword', 'English_IPA', 'English_Sound_Classes']]
etyma_englishdata.to_csv(
        Path(__file__).parent.parent / "data" / 'etyma_englishdata.tsv', sep='\t', index=False)

etyma_dutchdata = merged_etyma_dutch[['Headword', 'Dutch_IPA', 'Dutch_Sound_Classes']]
etyma_dutchdata.to_csv(
        Path(__file__).parent.parent / "data" / 'etyma_dutchdata.tsv', sep='\t', index=False)
