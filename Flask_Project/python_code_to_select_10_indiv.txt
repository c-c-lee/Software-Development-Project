# Importing the pandas library for data manipulation, particularly for handling the TSV file,
# and the vcf library for reading and writing VCF files.
import pandas as pd
import vcf

# Loading the cleaned sample population data from a TSV file. The data includes sample IDs and their corresponding populations.
# The 'sep' parameter specifies that the separator in the file is a tab character.
sample_pop_df = pd.read_csv('/Users/farzadhamzawe/group_project bioinformatics/Admixture_2/cleaned_sample_pop.tsv', sep='\t')

# Creating a dictionary to map each sample ID to its population. This will be crucial for processing the VCF file.
sample_to_population = dict(zip(sample_pop_df.ID, sample_pop_df.population))

# Defining file paths for the annotated VCF file to read from and the new VCF file to write to.
annotated_vcf_path = '/Users/farzadhamzawe/group_project bioinformatics/Admixture_2/annotated_vcf_file.vcf'
output_vcf_file = '/Users/farzadhamzawe/group_project bioinformatics/Admixture_2/selected_individuals.vcf'

# This function selects one individual per population from the annotated VCF file.
def select_individuals(annotated_vcf_path, sample_to_population):
    selected_individuals = {}  # Dictionary to hold the selected individual per population
    with open(annotated_vcf_path, 'r') as vcf_file:
        for line in vcf_file:
            # Identifying the header line that contains sample IDs
            if line.startswith('#CHROM'):
                headers = line.strip().split('\t')[9:]  # Extracting sample IDs, which start from the 10th column
                for sample in headers:
                    # Parsing the sample ID and its associated population information
                    sample_id, population_info = sample.split(' [')
                    population = population_info.rstrip(']')
                    # Selecting the first encountered individual for each population
                    if population not in selected_individuals:
                        selected_individuals[population] = sample_id
    return selected_individuals

# Running the selection function to get a dictionary of selected individuals, one per population.
selected_individuals = select_individuals(annotated_vcf_path, sample_to_population)

# This function writes a new VCF file containing only the selected individuals.
def write_selected_individuals_vcf(input_vcf_file, output_vcf_file, selected_individuals):
    with open(input_vcf_file, 'r') as f_in, open(output_vcf_file, 'w') as f_out:
        # Initializing the VCF reader and writer with the input and output files, respectively.
        vcf_reader = vcf.Reader(f_in)
        vcf_writer = vcf.Writer(f_out, vcf_reader)

        # Iterating through the VCF records in the input file
        for record in vcf_reader:
            # Filtering the samples in each record to include only the selected individuals
            new_record = record
            new_record.samples = [sample for sample in record.samples if sample.sample in selected_individuals.values()]
            # Writing the record to the output file if it contains selected samples
            if new_record.samples:
                vcf_writer.write_record(new_record)

# Calling the function to create the new VCF file with selected individuals.
write_selected_individuals_vcf(annotated_vcf_path, output_vcf_file, selected_individuals)

