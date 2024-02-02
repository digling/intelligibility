import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# control the text size in the plot below
sns.set_context("talk")



# Read the three datasets
dutch_data = pd.read_csv(
        Path(__file__).parent / "data" / "etyma_dutchdata.tsv", sep='\t'
        )
german_data = pd.read_csv(
        Path(__file__).parent / "data" / "etyma_germandata.tsv", 
        sep='\t')
english_data = pd.read_csv(
        Path(__file__).parent / "data" / "etyma_englishdata.tsv", 
        sep='\t')

# Load word embeddings from NumPy arrays
S_trainGER = np.load(Path(__file__).parent / "data" / "S_GER_etymamatrix.npy")
S_testDUT = np.load(Path(__file__).parent / "data" / "S_DUT_etymamatrix.npy")
S_testENG = np.load(Path(__file__).parent / "data" / "S_ENG_etymamatrix.npy")

# Create empty lists to store similarity scores and word pairs
similarity_scores = []
word_pairs = []

# Loop through the rows in one of the datasets (e.g., german_data)
for i in range(len(german_data)):
    german_word = german_data.iloc[i]['Headword']
    dutch_word = dutch_data.iloc[i]['Headword']
    english_word = english_data.iloc[i]['Headword']

    # Fetch word embeddings from the NumPy arrays
    german_embeddings = S_trainGER[i]
    dutch_embeddings = S_testDUT[i]
    english_embeddings = S_testENG[i]

    # Compute cosine similarity between German and Dutch embeddings
    similarity_score_ger_dut = cosine_similarity([german_embeddings], [dutch_embeddings])[0][0]

    # Compute cosine similarity between German and English embeddings
    similarity_score_ger_eng = cosine_similarity([german_embeddings], [english_embeddings])[0][0]

    # Compute cosine similarity between Dutch and English embeddings
    similarity_score_dut_eng = cosine_similarity([dutch_embeddings], [english_embeddings])[0][0]

    # Append the similarity scores and word pairs
    similarity_scores.append((similarity_score_ger_dut, similarity_score_ger_eng, similarity_score_dut_eng))
    word_pairs.append((german_word, dutch_word, english_word))

# Create a DataFrame from the similarity scores and word pairs
similarity_df = pd.DataFrame({'German_Word': [pair[0] for pair in word_pairs],
                              'Dutch_Word': [pair[1] for pair in word_pairs],
                              'English_Word': [pair[2] for pair in word_pairs],
                              'Similarity_German_Dutch': [score[0] for score in similarity_scores],
                              'Similarity_German_English': [score[1] for score in similarity_scores],
                              'Similarity_Dutch_English': [score[2] for score in similarity_scores]})

# Save the DataFrame to a CSV file
similarity_df.to_csv('similarity_results.csv', index=False)

# Create a KDE plot to visualize the distribution of similarity scores
plt.figure(figsize=(10, 6))
sns.kdeplot(data=similarity_df, x='Similarity_German_Dutch', fill=True, common_norm=False, label='German-Dutch', color='blue')
sns.kdeplot(data=similarity_df, x='Similarity_German_English', fill=True, common_norm=False, label='German-English', color='red')
sns.kdeplot(data=similarity_df, x='Similarity_Dutch_English', fill=True, common_norm=False, label='Dutch-English', color='green')
plt.xlabel('Cosine Similarity')
plt.ylabel('Density')
plt.title('Distribution of Cosine Similarity between Language Pairs')

# Move the legend to the upper left corner of the plot
plt.legend(loc='upper left')

plt.savefig("cosine-similarities.pdf")
