# Importing pandas, a powerful data manipulation library, to handle the TSV file.
import pandas as pd

# Loading the cleaned sample population data from a TSV file into a DataFrame.
# The 'sep' parameter specifies that the separator in the file is a tab character.
sample_pop_df = pd.read_csv('/Users/farzadhamzawe/group_project bioinformatics/Admixture_2/cleaned_sample_pop.tsv', sep='\t')

# Creating a dictionary to efficiently map each sample ID to its corresponding population.
# This will be useful for quickly annotating the VCF file with population information.
sample_to_population = dict(zip(sample_pop_df.ID, sample_pop_df.population))

# Defining a function to annotate a VCF file with population information for each sample.
def annotate_vcf(vcf_path, annotated_vcf_path, sample_to_population):
    # Opening the original VCF file for reading and a new file for writing the annotated VCF.
    with open(vcf_path, 'r') as vcf_file, open(annotated_vcf_path, 'w') as annotated_vcf:
        # Iterating over each line in the original VCF file.
        for line in vcf_file:
            # If the line is a metadata header (starting with ##), write it directly to the annotated file.
            if line.startswith('##'):
                annotated_vcf.write(line)
            # If the line is the column header (starting with # but not ##), it needs special handling.
            elif line.startswith('#'):
                headers = line.strip().split('\t')
                new_headers = headers[:9]  # Retaining the first 9 columns as is (standard VCF columns).
                # Appending population information to each sample column header in the VCF.
                for sample in headers[9:]:
                    # Using the sample_to_population dictionary to fetch the population, defaulting to 'Unknown' if not found.
                    population = sample_to_population.get(sample, 'Unknown')
                    new_headers.append(f'{sample} [{population}]')  # Format: SampleID [Population]
                # Writing the modified header line to the annotated VCF file.
                annotated_vcf.write('\t'.join(new_headers) + '\n')
            else:
                # For all other lines (actual variant data), write them directly to the annotated file.
                annotated_vcf.write(line)

# Specifying the file paths for the input VCF and the output annotated VCF.
vcf_path = '/Users/farzadhamzawe/group_project bioinformatics/chr1.vcf'
annotated_vcf_path = '/Users/farzadhamzawe/group_project bioinformatics/Admixture_2/annotated_vcf_file.vcf'

# Calling the annotate_vcf function to add population annotations to the VCF file.
# This enhances the VCF with valuable population context for each sample.
annotate_vcf(vcf_path, annotated_vcf_path, sample_to_population)
