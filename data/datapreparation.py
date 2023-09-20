import pandas as pd

#get Dutch and German vectors from numberbatch (https://github.com/commonsense/conceptnet-numberbatch) and create output files to work with (= .tsv)
# this reserach uses numberbatch version 19.08

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

#########

# Read in the numberbatch data you created with the code above
dutchvectors_numberbatch = pd.read_csv('/Users/jessicanieder/Desktop/Passau/Habil/Project_Germanic/data/dutchvectors_numberbatch.tsv',   delimiter="\s", engine='python')
print(dutchvectors_numberbatch)

#germanvectors_numberbatch = pd.read_table('germanvectors_numberbatch.tsv', delimiter="\s", engine='python')
#print(germanvectors_numberbatch) ##### this code takes a long time to load due to memory problems, I will read it in chunks instead

# Define the file path and specifiy the delimiter used in your file
file_path = '/Users/jessicanieder/Desktop/Passau/Habil/Project_Germanic/data/germanvectors_numberbatch.tsv'
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


# Read in CELEX data
celex_german = pd.read_csv("~/Desktop/Passau/Habil/Project_Germanic/preparation/celex-german.tsv", sep="\t")
celex_dutch = pd.read_csv("~/Desktop/Passau/Habil/Project_Germanic/preparation/celex-dutch.tsv", sep="\t")

# Take string in column 'V1' and only keep the relevant part (= the word form)
germanvectors_numberbatch['V1'] = germanvectors_numberbatch['V1'].str.replace("^.*/", "")
dutchvectors_numberbatch['V1'] = dutchvectors_numberbatch['V1'].str.replace("^.*/", "")

# Rename the CELEX column for the merging process
celex_german.rename(columns={"HEADWORD": "V1"}, inplace=True)
celex_dutch.rename(columns={"HEADWORD": "V1"}, inplace=True)

# Merge data and drop duplicated rows
merged_german = pd.merge(celex_german, germanvectors_numberbatch, on="V1")
merged_dutch = pd.merge(celex_dutch, dutchvectors_numberbatch, on="V1")

merged_german.drop_duplicates(inplace=True)
merged_dutch.drop_duplicates(inplace=True)

# Save data as .tsv
merged_german.to_csv('~/Desktop/Passau/Habil/Project_Germanic/germanCELEX_vectors.tsv', sep='\t', quotechar='"', quoting=0, index=False)
merged_dutch.to_csv('~/Desktop/Passau/Habil/Project_Germanic/dutchCELEX_vectors.tsv', sep='\t', quotechar='"', quoting=0, index=False)
               