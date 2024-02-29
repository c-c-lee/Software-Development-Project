# Importing the csv module to handle reading and writing of CSV/TSV files.
import csv

# A dictionary mapping population codes to their respective superpopulation codes.
# This serves as a reference for categorizing individual populations into broader superpopulations.
pop_to_superpop = {
    'CHB': 'EAS', 'JPT': 'EAS', 'CHS': 'EAS', 'CDX': 'EAS', 'KHV': 'EAS',
    'CEU': 'EUR', 'TSI': 'EUR', 'FIN': 'EUR', 'GBR': 'EUR', 'IBS': 'EUR', 'SIB': 'EUR',
    'YRI': 'AFR', 'LWK': 'AFR', 'MAG': 'AFR', 'MSL': 'AFR', 'ESN': 'AFR',
    'ASW': 'AFR', 'ACB': 'AFR', 'GWD': 'AFR',
    'MXL': 'AMR', 'PUR': 'AMR', 'CLM': 'AMR', 'PEL': 'AMR',
    'GIH': 'SAS', 'PJL': 'SAS', 'BEB': 'SAS', 'STU': 'SAS', 'ITU': 'SAS'
}

# This function reads an input file, adds a superpopulation code to each row based on
# the population code, and writes the result to an output file.
def add_superpopulation(input_file_path, output_file_path, pop_to_superpop):
    missing_superpops = set()  # A set to track any population codes not found in our mapping.

    # Opening the input file for reading and the output file for writing.
    with open(input_file_path, mode='r', newline='') as infile, \
            open(output_file_path, mode='w', newline='') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')  # Initializing a CSV reader with tab delimiter.
        writer = csv.writer(outfile, delimiter='\t')  # Initializing a CSV writer with tab delimiter.
        
        # Reading the header from the input file and appending 'Super Population' as a new column.
        header = next(reader)
        header.append('Super Population')
        writer.writerow(header)
        
        # Iterating over each row in the input file.
        for row in reader:
            pop_code = row[1][:3]  # Extracting the population code from the second column.
            superpop_code = pop_to_superpop.get(pop_code)  # Retrieving the corresponding superpopulation code.
            
            # If the population code is not in our mapping, mark it as 'Unknown' and record the missing code.
            if superpop_code is None:
                missing_superpops.add(pop_code)
                superpop_code = 'Unknown'
                
            row.append(superpop_code)  # Appending the superpopulation code to the row.
            writer.writerow(row)  # Writing the modified row to the output file.
    
    # After processing all rows, check if there were any population codes without a superpopulation mapping.
    if missing_superpops:
        # Print a warning listing all unique population codes that were not found in the mapping.
        print(f"Warning: Superpopulation codes not found for the following population codes: {', '.join(missing_superpops)}")

# Specifying the path to your input TSV file and the desired path for the output file.
input_file_path = '/Users/farzadhamzawe/group_project bioinformatics/admixture_3/270_selected_file.tsv'
output_file_path = '/Users/farzadhamzawe/group_project bioinformatics/admixture_3/270_selected_file_with_SP.tsv'

# Calling the function to add superpopulation information to the input file and save the result.
add_superpopulation(input_file_path, output_file_path, pop_to_superpop)
