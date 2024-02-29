import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
# Path to your SQLite database
db_path = 'instance/ArchGenome.db'
base_output_dir = 'static/heatmap'

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return "".join(c if c.isalnum() or c in ['_', '-', '.'] else '_' for c in filename)

def get_allele_frequency(snp_id, population_codes):
    """Retrieve allele frequencies for a given SNP ID and list of population codes."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    allele_freqs = {}

    for population_code in population_codes:
        # Query for allele frequencies
        cursor.execute('''
            SELECT REF, ALT
            FROM allele_frequency
            WHERE position IN (SELECT position FROM snp WHERE id = ?) AND population_code = ?
        ''', (snp_id, population_code))
        allele_freq = cursor.fetchone()
        allele_freqs[population_code] = allele_freq

    conn.close()

    return allele_freqs

def calculate_fst(population_codes, snp_ids):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    fst_values = []

    for snp_id in snp_ids:
        allele_frequencies = get_allele_frequency(snp_id, population_codes)

        # Calculate pairwise FST for each pair of populations
        for i in range(len(population_codes)):
            for j in range(i + 1, len(population_codes)):
                pop1, pop2 = population_codes[i], population_codes[j]
                allele_freq_pop1 = allele_frequencies[pop1]
                allele_freq_pop2 = allele_frequencies[pop2]

                # Check if there is variation in allele frequencies
                if allele_freq_pop1 and allele_freq_pop2:
                    ref_pop1, alt_pop1 = allele_freq_pop1
                    ref_pop2, alt_pop2 = allele_freq_pop2

                    # Calculate Weir and Cockerham's Fst
                    num = (alt_pop1 - alt_pop2)**2 + (ref_pop1 - ref_pop2)**2
                    den = (alt_pop1 + alt_pop2) * (ref_pop1 + ref_pop2)

                    fst_value = num / (2 * den) if den != 0 else 0
                    fst_values.append((snp_id, pop1, pop2, fst_value))
                    print(f"FST for SNP: {snp_id}, Populations: {pop1} vs {pop2}: {fst_value}")
                else:
                    print(f"No variation in allele frequencies for SNP: {snp_id}, Populations: {pop1} vs {pop2}")

    conn.close()

    return fst_values

def save_fst_results_to_dataframe(fst_values):
    columns = ["SNP_ID", "Population1", "Population2", "FST"]
    df = pd.DataFrame(fst_values, columns=columns)
    return df

def save_dataframe_to_file(df, filename):
    df.to_csv(filename, index=False)

def create_fst_heatmap(df, snp_id):
    populations = list(set(df["Population1"].tolist() + df["Population2"].tolist()))
    df_pivot = pd.DataFrame(index=populations, columns=populations)

    for _, row in df.iterrows():
        pop1, pop2, fst_value = row["Population1"], row["Population2"], row["FST"]
        df_pivot.loc[pop1, pop2] = fst_value
        df_pivot.loc[pop2, pop1] = fst_value

    plt.figure(figsize=(10, 8))
    sns.heatmap(df_pivot.astype(float), annot=True, cmap="coolwarm", fmt=".3f", linewidths=.5)
    plt.title(f"FST Heatmap for SNP {snp_id}")

    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)
    
    # Save the heatmap as an image file
    sanitized_snp_id = sanitize_filename(snp_id)
    
    # Save the heatmap as an image file
    image_name = f'heatmap_{sanitized_snp_id}.png'
    save_path = os.path.join(base_output_dir, image_name)
    plt.savefig(save_path)

    return image_name
