import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt

#### Check semantic similarity of numberbatch vectors for the comparative-wordlist.tsv data

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
comparative_data = pd.read_csv('comparative-wordlist.tsv',   delimiter="\t", engine='python')

# I take the Dutch words and German words out of it to merge separately to create two data sets with their vectors
comparative_data_german = comparative_data[['German_Entry']]
comparative_data_german['German_Entry'] = comparative_data_german['German_Entry'] .str.lower() #numberbatch doesn't have capital letters for German nouns, I will change to lowercase
comparative_data_dutch = comparative_data[['Dutch_Entry']]

# Rename the column for the merging process
germanvectors_numberbatch.rename(columns={"V1": "German_Entry"}, inplace=True)
dutchvectors_numberbatch.rename(columns={"V1" : "Dutch_Entry"}, inplace=True)

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
print(rows_with_nan_dutch)# 625 win#gerd

#German
rows_with_nan_german = mergcomparative_data_german[mergcomparative_data_german.isna().any(axis=1)]
print(rows_with_nan_german)

#63          gesäß
#73        meißeln
#74         gießen
#87         meißel
#204      fußboden
#216           fuß
#243     großvater
#244    großmutter
#457        stoßen

# Delete rows with NaN values from mergcomparative_data_german
mergcomparative_data_german = mergcomparative_data_german.dropna()

# Delete rows with NaN values from mergcomparative_data_dutch
mergcomparative_data_dutch = mergcomparative_data_dutch.dropna()

# I will delete the German and Dutch counterparts for the missing values above from the data to have the same amount of words with their respective counterparts
# Define the value you want to use as the condition for deletion
to_delete_ingerman = "weinstock"  # German counterpart of # 625 win#gerd
to_delete_indutch = ["billen", "kerven", "gieten", "beitel", "vloer", "voet", "grootvader", "grootmoeder", "duwen"] # Dutch counterparts of list above
# Delete rows where column 'X_Entry' matches the specified value
mergcomparative_data_dutch = mergcomparative_data_dutch[~mergcomparative_data_dutch['Dutch_Entry'].isin(to_delete_indutch)]
mergcomparative_data_german = mergcomparative_data_german[mergcomparative_data_german['German_Entry'] != to_delete_ingerman]
# checking the rows shows me that vloer appears two times in the Dutch list and is now deleted
# I delete the German counterpart Diele as well
to_delete_ingerman2 = "diele"
mergcomparative_data_german = mergcomparative_data_german[mergcomparative_data_german['German_Entry'] != to_delete_ingerman2]

# export the merged DataFrames if necessary
# mergcomparative_data_german.to_csv('mergedgerman.csv', index=False)
# mergcomparative_data_dutch.to_csv('mergeddutch.csv', index=False)


###### now I have two DataFrames containing translation equivalents with their numberbatch vectors
# I will compute cosine similarites for the pairs of words

# Create an empty list to store similarity scores and a list for word pairs
similarity_scores = []
word_pairs = []

# Loop through each row in both dataframes
for i in range(len(mergcomparative_data_german)):
    german_word = mergcomparative_data_german.iloc[i]['German_Entry']
    dutch_word = mergcomparative_data_dutch.iloc[i]['Dutch_Entry']
    
    german_embeddings = mergcomparative_data_german.iloc[i, 1:]  # word embeddings start from column V2
    dutch_embeddings = mergcomparative_data_dutch.iloc[i, 1:]   # word embeddings start from column V2
    
    # Compute cosine similarity between embeddings
    similarity_score = cosine_similarity([german_embeddings], [dutch_embeddings])[0][0]
    
    # Append the similarity score and word pair to the lists
    similarity_scores.append(similarity_score)
    word_pairs.append((german_word, dutch_word))

# Create a DataFrame from the similarity scores and my word pairs
similarity_df = pd.DataFrame({'German_Word': [pair[0] for pair in word_pairs],
                              'Dutch_Word': [pair[1] for pair in word_pairs],
                              'Similarity': similarity_scores})

# Save the DataFrame to a CSV file if needed to be accessed later
# similarity_df.to_csv('similarity_results.csv', index=False)


# Create a KDE plot to visualize the distribution of similarity scores
plt.figure(figsize=(10, 6))
sns.kdeplot(data=similarity_df, x='Similarity', fill=True, common_norm=False, palette="viridis")
plt.xlabel('Cosine Similarity')
plt.ylabel('Density')
plt.title('Distribution of Cosine Similarity between Dutch and German Word Pairs')
plt.show()