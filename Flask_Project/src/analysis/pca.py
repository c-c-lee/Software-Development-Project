import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_pca_data(filepath):
    pca_data = pd.read_csv(filepath, sep='\t')
    return pca_data

def plot_pca(pca_data, selection, selection_type, output_path):
    """
    Plots PCA based on user selection and saves the plot to a file.

    Args:
    - pca_data (DataFrame): The PCA data loaded from the file.
    - selection (str): The superpopulation or population selected by the user.
    - selection_type (str): Either 'Superpopulation' or 'Population' indicating the type of selection.
    - output_path (str): The file path to save the plot image.
    """
    # Filter data based on selection
    if selection_type == 'Superpopulation':
        filtered_data = pca_data[pca_data['Superpopulation'] == selection]
    elif selection_type == 'Population':
        filtered_data = pca_data[pca_data['Population'] == selection]
    else:
        raise ValueError("Invalid selection type. Please choose 'Superpopulation' or 'Population'.")

    # Plotting
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='PC1', y='PC2', hue=selection_type, data=filtered_data, palette='tab10', legend='full', s=100)
    plt.title(f'PCA Plot for {selection} ({selection_type})')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.axhline(y=0, color='k', linestyle='--', lw=1)
    plt.axvline(x=0, color='k', linestyle='--', lw=1)
    plt.grid(True)
    
    # Save the plot instead of showing it
    plt.savefig(output_path)
    plt.close()
