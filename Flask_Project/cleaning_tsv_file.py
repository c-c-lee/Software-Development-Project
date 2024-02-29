# This function is designed by me (Farzard Hamzawe) to clean up TSV files. 
# Its main purpose is to ensure that each line in the TSV contains only 
# one tab character between the sample ID and the population,
# which is crucial for maintaining data integrity in downstream processes.
def clean_tsv_file(tsv_file_path, cleaned_tsv_file_path):
    # Opening the original TSV file for reading and a new file for writing the cleaned data.
    with open(tsv_file_path, 'r') as input_file, open(cleaned_tsv_file_path, 'w') as output_file:
        # Reading the first line, which is the header, and writing it directly to the cleaned file.
        
        header = input_file.readline()
        output_file.write(header)

        # Iterating over each subsequent line in the original TSV file.
        for line in input_file:
            # Removing any leading or trailing whitespace and splitting the line by tabs.
            parts = line.strip().split('\t')
            
            # Ensuring the line is correctly formatted with exactly two parts: sample ID and population.
            if len(parts) == 2:
                sample_id, population = parts
                # Reconstructing the line with a single tab between the sample ID and population,
                # then writing this cleaned line to the new file.
                cleaned_line = f"{sample_id}\t{population}\n"
                output_file.write(cleaned_line)

# Specifying the path to the original TSV file and the path where the cleaned file will be saved.
# These paths are hardcoded for now but can be parameterized if the script is expanded.
tsv_file_path = '/Users/farzadhamzawe/group_project bioinformatics/sample_pop.tsv'
cleaned_tsv_file_path = '/Users/farzadhamzawe/group_project bioinformatics/Admixture_2/cleaned_sample_pop.tsv'


clean_tsv_file(tsv_file_path, cleaned_tsv_file_path)

# Printing a confirmation message with the path to the cleaned file,
print(f"Cleaned TSV file saved to: {cleaned_tsv_file_path}")
