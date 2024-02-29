import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

pca_data_filepath = 'tables/pca_scores.tsv'
base_output_dir = 'static/imagepca'

mapping = {
    "East Asian": "EAS",
    "Europe": "EUR",
    "Ad Mixed American": "AMR",
    "African": "AFR",
    "South Asian": "SAS"
}

population_mapping = {'Siberian': 'SIB', 'British in England and Scotland': 'GBR', 'Finnish in Finland': 'FIN', 'Southern Han Chinese': 'CHS', 'Puerto Rican from Puerto Rico': 'PUR', 'Chinese Dai in Xishuangbanna, China': 'CDX', 'Colombian from Medellin, Colombia': 'CLM', 'Iberian population in Spain': 'IBS', 'Peruvian from Lima, Peru': 'PEL', 'Punjabi from Lahore, Pakistan': 'PJL', 'Kinh in Ho Chi Minh City, Vietnam': 'KHV', 'African Caribbean in Barbados': 'ACB', 'Gambian in Western Division, Gambia': 'GWD', 'Esan in Nigeria': 'ESN',
                      'Bengali from Bangladesh': 'BEB', 'Mende in Sierra, Leone': 'MSL', 'Sri Lankan Tamil from the UK': 'STU', 'Indian Telugu from the UK': 'ITU', 'Utah Residents (CEPH) with Northern and Western European ancestry': 'CEU', 'Yoruba in Ibadan, Nigeria': 'YRI', 'Han Chinese in Beijing, China': 'CHB', 'Japanese in Tokyo, Japan': 'JPT', 'Luhya in Webuye, Kenya': 'LWK', "American's of African Ancestry in SW, USA": 'ASW', 'Mexican Ancestry from Los Angeles, USA': 'MXL', 'Toscani in Italia': 'TSI', 'Gujarati Indian from Houston, Texas': 'GIH'}


def load_pca_data(filepath):
    pca_data = pd.read_csv(filepath, sep='\t')
    return pca_data


def plot_pca(pca_data, selection, selection_type, base_output_dir):
    """
    Plots PCA based on user selection and saves the plot to a file in the specified directory.

    Args:
    - pca_data (DataFrame): The PCA data loaded from the file.
    - selection (str): The superpopulation or population selected by the user.
    - selection_type (str): Either 'Superpopulation' or 'Population' indicating the type of selection.
    - base_output_dir (str): The base directory to save the plot image.
    """
    if selection_type == 'Superpopulation':
        filtered_data = pca_data[pca_data['Superpopulation'] == selection]
        # Use 'Population' as the hue to differentiate populations within a superpopulation
        hue_col = 'Population'
    elif selection_type == 'Population':
        filtered_data = pca_data[pca_data['Population'] == selection]
        # Use 'Population' type as hue, but it will be uniform since it's one population
        hue_col = selection_type
    else:
        raise ValueError(
            "Invalid selection type. Please choose 'Superpopulation' or 'Population'.")

    # Plotting
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='PC1', y='PC2', hue=hue_col,
                    data=filtered_data, palette='tab10', legend='full', s=100)
    plt.title(f'PCA Plot for {selection} ({selection_type})')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.axhline(y=0, color='k', linestyle='--', lw=1)
    plt.axvline(x=0, color='k', linestyle='--', lw=1)
    plt.grid(True)

    # Construct the output path using the base directory
    output_filename = f"PCA_{selection}_{selection_type}.png".replace(
        ' ', '_').replace('/', '_')
    output_path = os.path.join(base_output_dir, output_filename)
    # Save the plot
    plt.savefig(output_path)
    plt.close()
    print(f"Plot saved to: {output_path}")
    return output_filename


def main(selection_string, selection_type):
    """
    Main function to process the selection_string and generate the PCA plot.

    Args:
    - selection_string (str): The population or superpopulation name.
    """
    pca_data = load_pca_data(pca_data_filepath)
    # Simple check to determine if the input is a superpopulation or population
    unique_superpopulations = pca_data['Superpopulation'].unique()
    unique_populations = pca_data['Population'].unique()

    if selection_string in mapping:
        selection_string = mapping[selection_string]
    elif selection_string in population_mapping:
        selection_string = population_mapping[selection_string]

    if selection_string in unique_superpopulations:
        output_filename = plot_pca(
            pca_data, selection_string, 'Superpopulation', base_output_dir)
    elif selection_string in unique_populations:
        output_filename = plot_pca(
            pca_data, selection_string, 'Population', base_output_dir)
    else:
        print("Invalid input: The selection does not match any known population or superpopulation.")
    return output_filename

# main("") to check if it works, put superpopulation or population in there