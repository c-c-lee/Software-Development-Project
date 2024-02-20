import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def calculate_pairwise_fst(data, output_file_path='C:/Users/siril/Group Project/Software-Development-Project/Flask_Project/static/paiwise_fst.txt'):
    # Create a dictionary to store allele frequencies for each population
    allele_freqs = {}

    # Separate allele frequencies by SNP and population
    for snp, pop, rf, af in data:
        if snp not in allele_freqs:
            allele_freqs[snp] = {}
        if pop not in allele_freqs[snp]:
            allele_freqs[snp][pop] = {'RF': [], 'AF': []}
        allele_freqs[snp][pop]['RF'].append(rf)
        allele_freqs[snp][pop]['AF'].append(af)

    # Create a DataFrame to store pairwise FST values
    populations = list(allele_freqs[next(iter(allele_freqs))].keys())
    pairwise_fst_matrix = pd.DataFrame(index=populations, columns=populations)

    # Iterate over population pairs
    for i in range(len(populations)):
        for j in range(i + 1, len(populations)):
            pop1 = populations[i]
            pop2 = populations[j]

            # Initialize lists to store FST values for each SNP
            fst_values = []

            # Iterate over SNPs
            for snp, freqs in allele_freqs.items():
                # Calculate average ref and alt frequencies across all populations for the current SNP
                avg_rf = sum(freqs[pop]['RF'][0] for pop in populations) / len(populations)
                avg_af = sum(freqs[pop]['AF'][0] for pop in populations) / len(populations)

                # Calculate Ht
                ht = 2 * avg_rf * avg_af

                # Calculate Hs for each population in the pair
                hs_pop1 = 2 * freqs[pop1]['RF'][0] * freqs[pop1]['AF'][0]
                hs_pop2 = 2 * freqs[pop2]['RF'][0] * freqs[pop2]['AF'][0]
                hs = (hs_pop1 + hs_pop2) / 2

                # Calculate pairwise FST
                if ht == 0:
                    fst = np.nan
                else:
                    fst = (ht - hs) / ht

                fst_values.append(fst)

            # Average FST values across all SNPs for the current pair of populations
            avg_fst = np.nanmean(fst_values)

            # Store the average FST value in the matrix
            pairwise_fst_matrix.at[pop1, pop2] = avg_fst
            pairwise_fst_matrix.at[pop2, pop1] = avg_fst

    # Plot the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(pairwise_fst_matrix.astype(float), annot=True, cmap="viridis", linewidths=.5, fmt=".3f")
    plt.title('Pairwise FST Matrix')
    plt.show()

    # Save pairwise FST values to a text file 
    pairwise_fst_matrix.to_csv(output_file_path, sep='\t', float_format='%.3f')

    # Return the pairwise FST matrix heatmap and text file to static directory(used for download link)
    return pairwise_fst_matrix






