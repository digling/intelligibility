import pandas as pd

# ATTENTION this script requires to download numberbatch with download_numberbatch.sh first
# txt file too large to uploaded to git

# Define column names (V1= word form column, V2-V301= word vectors)
column_names = [f'V{i}' for i in range(1, 302)]  

# Initialize lists to store German, Dutch, and English data
german_data = []
dutch_data = []
english_data = []

# Read and process the numberbatch input file
with open('numberbatch.txt', 'r', encoding='utf-8') as input_file:
    for line in input_file:
        if '/de/' in line:
            # Split the input line into columns based on tabs
            columns = line.strip().split('\t')
            german_data.append(columns)
        elif '/nl/' in line:
            # Split the input line into columns based on tabs
            columns = line.strip().split('\t')
            dutch_data.append(columns)
        elif '/en/' in line:
            # Split the input line into columns based on tabs
            columns = line.strip().split('\t')
            english_data.append(columns)

# Save the data as separate TSV files for German, Dutch, and English
def save_data_as_tsv(data, filename):
    with open(filename, 'w', encoding='utf-8') as output_file:
        # Write the header row with tab-separated column names
        header_row = '\t'.join(column_names) + '\n'
        output_file.write(header_row)
        # Write the data rows
        for row in data:
            output_file.write('\t'.join(row) + '\n')

# Save German data
save_data_as_tsv(german_data, 'germanvectors_numberbatch.tsv')

# Save Dutch data
save_data_as_tsv(dutch_data, 'dutchvectors_numberbatch.tsv')

# Save English data
save_data_as_tsv(english_data, 'englishvectors_numberbatch.tsv')