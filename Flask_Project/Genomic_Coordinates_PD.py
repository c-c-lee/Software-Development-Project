import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Path to your SQLite database
db_path = 'instance/ArchGenome.db'
base_output_dir = 'static/heatmap'

def get_allele_frequency_by_position(position, population_codes):
    """Retrieve allele frequencies for a given genomic position and list of population codes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    allele_freqs = {population: [] for population in population_codes}

    for population_code in population_codes:
        # Query for allele frequencies
        cursor.execute('''
            SELECT REF, ALT
            FROM allele_frequency
            WHERE position = ? AND population_code = ?
        ''', (position, population_code))
        allele_freq = cursor.fetchall()
        allele_freqs[population_code] = allele_freq

    conn.close()

    return allele_freqs

def calculate_fst(population_codes, positions):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    fst_values = []

    for position in positions:
        allele_frequencies = get_allele_frequency_by_position(position, population_codes)

        # Calculate pairwise FST for each pair of populations
        for i in range(len(population_codes)):
            for j in range(len(population_codes)):
                pop1, pop2 = population_codes[i], population_codes[j]
                allele_freq_pop1 = allele_frequencies[pop1]
                allele_freq_pop2 = allele_frequencies[pop2]

                # Check if there is variation in allele frequencies
                if allele_freq_pop1 and allele_freq_pop2:
                    ref_pop1, alt_pop1 = zip(*allele_freq_pop1)
                    ref_pop2, alt_pop2 = zip(*allele_freq_pop2)

                    # Calculate Weir and Cockerham's Fst
                    num = (sum(alt_pop1) - sum(alt_pop2))**2 + (sum(ref_pop1) - sum(ref_pop2))**2
                    den = (sum(alt_pop1) + sum(alt_pop2)) * (sum(ref_pop1) + sum(ref_pop2))

                    fst_value = num / (2 * den) if den != 0 else 0
                    fst_values.append((position, pop1, pop2, fst_value))
                    print(f"FST for Position: {position}, Populations: {pop1} vs {pop2}: {fst_value}")
                else:
                    print(f"No variation in allele frequencies for Position: {position}, Populations: {pop1} vs {pop2}")

    conn.close()

    return fst_values

def save_fst_results_to_dataframe(fst_results):
    df = pd.DataFrame(fst_results, columns=["Position", "Population1", "Population2", "FST"])
    return df

def plot_heatmap(df_fst, position):
    # Filter DataFrame for the specific position
    df_filtered = df_fst[df_fst['Position'] == position]

    # Pivot the DataFrame to prepare for heatmap
    df_pivot = df_filtered.pivot(index='Population1', columns='Population2', values='FST')

    # Plot the heatmap
    sns.heatmap(df_pivot, annot=True, cmap="coolwarm", fmt=".3f", linewidths=.5)
    plt.title(f'Pairwise FST between Populations for Genomic Position {position}')

    position = str(position)
    image_name = f'heatmap_{position}.png'
    save_path = os.path.join(base_output_dir, image_name)
    plt.savefig(save_path)

    return image_name

# # Test the calculate_fst function with multiple populations and genomic positions
# population_codes = ["JPT", "GBR", "MXL"]
# positions = [10437, 10438]  # Replace with the actual genomic positions
# fst_results = calculate_fst(population_codes, positions)

# # Save the FST results to a DataFrame
# df_fst = save_fst_results_to_dataframe(fst_results)
# print(df_fst)

# # Save the DataFrame to a text file
# df_fst.to_csv('fst_results_positions.txt', sep='\t', index=False)

# # Plot individual heatmaps for each position
# for position in positions:
#     plot_heatmap(df_fst, position)
