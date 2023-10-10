import pandas as pd

# ATTENTION this script requires to download numberbatch with download_numberbatch.sh first
# txt file too large to uploaded to git

#get Dutch and German vectors from numberbatch and create output files (= .tsv)
with open('numberbatch.txt', 'r', encoding='utf-8') as input_file:
    with open('germanvectors_numberbatch.tsv', 'w', encoding='utf-8') as german_output_file:
        with open('dutchvectors_numberbatch.tsv', 'w', encoding='utf-8') as dutch_output_file:
            for line in input_file:
                if '/de/' in line:
                    # Split the line into columns based on tabs
                    columns = line.strip().split('\t')
                    # Write the columns to the German output file
                    german_output_file.write('\t'.join(columns) + '\n')
                elif '/nl/' in line:
                    # Split the line into columns based on tabs
                    columns = line.strip().split('\t')
                    # Write the columns to the Dutch output file
                    dutch_output_file.write('\t'.join(columns) + '\n')



## Define column names (V1= word form column, V2-V301= word vectors)
column_names = [f'V{i}' for i in range(1, 302)]  

# Initialize lists to store German and Dutch data
german_data = []
dutch_data = []

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

# Write the data to the German output file
with open('germanvectors_numberbatch.tsv', 'w', encoding='utf-8') as german_output_file:
    # Write the header row with tab-separated column names
    header_row = '\t'.join(column_names) + '\n'
    german_output_file.write(header_row)
    # Write the data rows
    for row in german_data:
        german_output_file.write('\t'.join(row) + '\n')

# Write the data to the Dutch output file
with open('dutchvectors_numberbatch.tsv', 'w', encoding='utf-8') as dutch_output_file:
    # Write the header row with tab-separated column names
    header_row = '\t'.join(column_names) + '\n'
    dutch_output_file.write(header_row)
    # Write the data rows
    for row in dutch_data:
        dutch_output_file.write('\t'.join(row) + '\n')

# data is stored as .tsv files
