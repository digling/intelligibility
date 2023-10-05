import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt

###### compute semantic similarities

# Read in numberbatch data
mergcomparative_data_german = pd.read_csv('/data/comparative_germandata.csv',   delimiter=",", engine='python')
mergcomparative_data_dutch = pd.read_csv('/data/comparative_dutchdata.csv',   delimiter=",", engine='python')


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
 similarity_df.to_csv('/data/similarity_results.csv', index=False)


# Create a KDE plot to visualize the distribution of similarity scores
plt.figure(figsize=(10, 6))
sns.kdeplot(data=similarity_df, x='Similarity', fill=True, common_norm=False, palette="viridis")
plt.xlabel('Cosine Similarity')
plt.ylabel('Density')
plt.title('Distribution of Cosine Similarity between Dutch and German Word Pairs')
plt.show()