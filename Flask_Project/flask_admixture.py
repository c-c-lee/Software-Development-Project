import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.ioff()

# Set the absolute path to your database
app_root_dir = 'C:/Users/ayush/OneDrive/Documents/Software-Development-Project'
db_path = "instance/ArchGenome.db"
images_dir = "static/images"

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

def get_population_full_name(population_code):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM population WHERE population_code = ?", (population_code,))
        result = cursor.fetchone()
        return result[0] if result else None
    
# Function to plot admixture data for a specific population with sample labels and smaller gaps between bars
def plot_admixture_with_sample_labels(admixture_data, k_value, colors, population_code):
    full_population_name = get_population_full_name(population_code)  # This fetches the full name based on the population code

    # Ensure the data is for 10 individuals, truncate if more, pad with zeros if less.
    print(f"Data received for plotting: {admixture_data.head()}")
    admixture_data = admixture_data.head(10)
    num_samples = len(admixture_data)
    if num_samples < 10:
        # If less than 10 samples, append rows with zeros
        padding = pd.DataFrame(0, index=range(10 - num_samples), columns=admixture_data.columns)
        admixture_data = pd.concat([admixture_data, padding], ignore_index=True)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 6), dpi=300)  # Adjust the figure size as necessary

    # Define the width of each bar and the smaller gap between them
    bar_width = 0.8

    # Plot each individual's ancestry proportions as stacked bars
    for i in range(10):
        bottom = 0
        # Calculate the position of the bar taking into account the smaller gap
        bar_position = i  # Each bar is now 1 unit apart
        for color, value in zip(colors, admixture_data.iloc[i, 3:]):  # Skip ID, Population Code, Super Population columns
            ax.bar(bar_position, value, bottom=bottom, color=color, width=bar_width)
            bottom += value
    
   
    
    # Set the x-ticks to be the middle of each bar
    tick_positions = [i for i in range(10)]
    sample_labels = [f'Sample {i+1}' for i in range(10)]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(sample_labels, rotation=45, ha='center', fontsize=10)

    # Set the xlabel to '[Population] Population'
    ax.set_xlabel(f'{full_population_name} Population', fontsize=12)

    # Set the y-label and title
    ax.set_ylabel('Ancestry Proportion', fontsize=12)
    ax.set_title(f'Admixture Results K={k_value}', fontsize=14) 

    # Create a legend with colored patches
    legend_patches = [mpatches.Patch(color=colors[i], label=f'Ancestry {i+1}') for i in range(len(colors))]
    ax.legend(handles=legend_patches, bbox_to_anchor=(1.1, 0.5), loc='upper left', title='Ancestries', fontsize=10)
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    plot_filename = f'admixture_{population_code}_k{k_value}.png'.replace(' ', '_')
    plot_path = os.path.join(images_dir, plot_filename)
    print(f"Saving plot to: {plot_path}")
    plt.savefig(plot_path, bbox_inches='tight', dpi=300)
    plt.savefig(plot_path)
    plt.close()  # Close the plot to free up memory
    return plot_filename  # Return the filename of the saved plot

def get_superpopulation_full_name(superpopulation):
    code_to_superpopulation_name = {
        'EAS': 'East Asian',
        'EUR': 'Europe',
        'AMR': 'Ad Mixed American',
        'AFR': 'African',
        'SAS': 'South Asian'
    }
    return code_to_superpopulation_name.get(superpopulation)

# Function to plot admixture data for a specific superpopulation
def plot_admixture_for_superpopulation(superpopulation):
    superpopulation_full_name = get_superpopulation_full_name(superpopulation)
    with sqlite3.connect(db_path) as conn:
        # Query the database to retrieve admixture data for k=3 and k=5 for the specified superpopulation
        query_k3 = f"SELECT * FROM admixture_k3 WHERE superpopulation = ?"
        admixture_k3 = pd.read_sql_query(query_k3, conn, params=(superpopulation,))

        query_k5 = f"SELECT * FROM admixture_k5 WHERE superpopulation = ?"
        admixture_k5 = pd.read_sql_query(query_k5, conn, params=(superpopulation,))

    # Sort the data by population code for consistent plotting
    admixture_k3.sort_values(by=['population_code'], inplace=True)
    admixture_k5.sort_values(by=['population_code'], inplace=True)

    # Define colors for each ancestry component
    colors_k3 = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Colors for k=3
    colors_k5 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Colors for k=5

    # Create figure and axis for k=3
    fig_k3, ax_k3 = plt.subplots(figsize=(20, 15), dpi=300)   # Adjust the figure size as necessary

    # Initialize the x position for the bars and list for x-tick positions for k=3
    x_pos_k3 = 0
    tick_positions_k3 = []
    tick_labels_k3 = []

    # Iterate over the grouped data by population code for k=3
    for pop_code_group, group_data_k3 in admixture_k3.groupby('population_code'):
        full_population_name = get_population_full_name(pop_code_group)
        group_indices_k3 = group_data_k3.index.tolist()
        num_individuals_k3 = len(group_indices_k3)
        start_x_pos_k3 = x_pos_k3  # Starting x position for the population code group for k=3

        # Plot each individual's ancestry proportions as stacked bars for k=3
        for _, row_k3 in group_data_k3.iterrows():
            bottom_k3 = 0
            # Stack the ancestry proportion for each individual for k=3
            for j, color_k3 in enumerate(colors_k3):
                value_k3 = row_k3.iloc[j + 3]  # Adjusted index based on the database structure for k=3
                ax_k3.bar(x_pos_k3, value_k3, bottom=bottom_k3, color=color_k3, width=0.8)  # Adjusted width for k=3
                bottom_k3 += value_k3
            x_pos_k3 += 1  # Increment the x position for the next individual for k=3

        # Add a tick position for the current group at the midpoint for k=3
        mid_x_pos_k3 = start_x_pos_k3 + (num_individuals_k3 / 2) - 0.5
        tick_positions_k3.append(mid_x_pos_k3)
        tick_labels_k3.append(full_population_name)

        # Add a thick black line to separate population code groups for k=3
        if x_pos_k3 < admixture_k3.shape[0]:
            ax_k3.axvline(x_pos_k3 - 1.5, color='black', linewidth=2)

    # Set the x-ticks to be in the middle of each population code group for k=3
    ax_k3.set_xticks(tick_positions_k3)
    ax_k3.set_xticklabels(tick_labels_k3, rotation=20, ha='right', fontsize=10) # Adjusted alignment to 'center' for k=3

    # Set other labels and title for k=3
    ax_k3.set_xlabel('Population', fontsize=25)
    ax_k3.tick_params(axis='y', labelsize=10)
    ax_k3.set_ylabel('Ancestry Proportion', fontsize=25)
    ax_k3.set_title(f'Admixture Results for Superpopulation: {superpopulation_full_name} K=3', fontsize=30)

    # Create a legend with colored patches for k=3
    legend_patches_k3 = [mpatches.Patch(color=colors_k3[i], label=f'Ancestry {i+1}') for i in range(len(colors_k3))]
    ax_k3.legend(handles=legend_patches_k3, bbox_to_anchor=(1, 1), loc='upper left', fontsize="medium")

    # Save the k3 plot
    plot_filename_k3 = f'admixture_{superpopulation}_k3.png'
    plot_path_k3 = os.path.join(images_dir, plot_filename_k3)
    plt.savefig(plot_path_k3, dpi=300) 
    plt.close(fig_k3)

    # Create figure and axis for k=5
    fig_k5, ax_k5 = plt.subplots(figsize=(20, 15), dpi=300)  # Increased resolution with dpi  # Adjust the figure size as necessary

    # Initialize the x position for the bars and list for x-tick positions for k=5
    x_pos_k5 = 0
    tick_positions_k5 = []
    tick_labels_k5 = []

    # Iterate over the grouped data by population code for k=5
    for pop_code_k5, group_data_k5 in admixture_k5.groupby('population_code'):
        full_population_name = get_population_full_name(pop_code_group)
        group_indices_k5 = group_data_k5.index.tolist()
        num_individuals_k5 = len(group_indices_k5)
        start_x_pos_k5 = x_pos_k5  # Starting x position for the population code group for k=5

        # Plot each individual's ancestry proportions as stacked bars for k=5
        for _, row_k5 in group_data_k5.iterrows():
            bottom_k5 = 0
            # Stack the ancestry proportion for each individual for k=5
            for j, color_k5 in enumerate(colors_k5):
                value_k5 = row_k5.iloc[j + 3]  # Adjusted index based on the database structure for k=5
                ax_k5.bar(x_pos_k5, value_k5, bottom=bottom_k5, color=color_k5, width=0.8)  # Adjusted width for k=5
                bottom_k5 += value_k5
            x_pos_k5 += 1  # Increment the x position for the next individual for k=5

        # Add a tick position for the current group at the midpoint for k=5
        mid_x_pos_k5 = start_x_pos_k5 + (num_individuals_k5 / 2) - 0.5
        tick_positions_k5.append(mid_x_pos_k5)
        tick_labels_k5.append(full_population_name)

        # Add a thick black line to separate population code groups for k=5
        if x_pos_k5 < admixture_k5.shape[0]:
            ax_k5.axvline(x_pos_k5 - 1.5, color='black', linewidth=2)

    # Set the x-ticks to be in the middle of each population code group for k=5
    ax_k5.set_xticks(tick_positions_k5)
    ax_k5.tick_params(axis='y', labelsize=10)
    ax_k5.set_xticklabels(tick_labels_k5, rotation=20, ha='right', fontsize=10)  # Adjusted alignment to 'center' for k=5

    # Set other labels and title for k=5
    ax_k5.set_xlabel('Population', fontsize=25)
    ax_k5.set_ylabel('Ancestry Proportion', fontsize=25)
    ax_k5.set_title(f'Admixture Results for Superpopulation: {superpopulation_full_name} K=5', fontsize=30)

    # Create a legend with colored patches for k=5
    legend_patches_k5 = [mpatches.Patch(color=colors_k5[i], label=f'Ancestry {i+1}') for i in range(len(colors_k5))]
    ax_k5.legend(handles=legend_patches_k5, bbox_to_anchor=(1, 1), loc='upper left', fontsize="medium")

    # Save the k5 plot
    plot_filename_k5 = f'admixture_{superpopulation}_k5.png'
    plot_path_k5 = os.path.join(images_dir, plot_filename_k5)
    plt.savefig(plot_path_k5, dpi=300)
    plt.close(fig_k5)

    return [plot_filename_k3, plot_filename_k5]

def get_population_code(full_name):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT population_code FROM population WHERE name = ?", (full_name,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_superpopulation_code(full_name):
    superpopulation_name_to_code = {
        'East Asian': 'EAS',
        'Europe': 'EUR',
        'Ad Mixed American': 'AMR',
        'African': 'AFR',
        'South Asian': 'SAS'
    }
    return superpopulation_name_to_code.get(full_name)



    
def check_input(input_value):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Check if the input is a population code or a superpopulation
    population_query = "SELECT DISTINCT population_code FROM admixture_k3 WHERE population_code=?"
    superpopulation_query = "SELECT DISTINCT superpopulation FROM admixture_k3 WHERE superpopulation=?"
    
    is_population = pd.read_sql_query(population_query, conn, params=(input_value,)).shape[0] > 0
    is_superpopulation = pd.read_sql_query(superpopulation_query, conn, params=(input_value,)).shape[0] > 0
    
    conn.close()
    return is_population, is_superpopulation

# Function to fetch and plot admixture data for a specific population code
def main_population_code(population_code):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Fetch data from the database for the specified population code
    query = "SELECT * FROM admixture_k3 WHERE population_code=?"
    admixture_k3 = pd.read_sql_query(query, conn, params=(population_code,))
    
    query = "SELECT * FROM admixture_k5 WHERE population_code=?"
    admixture_k5 = pd.read_sql_query(query, conn, params=(population_code,))
    
    conn.close()
    
    # Define colors for each ancestry component
    colors_k3 = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Colors for k=3
    colors_k5 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']  # Colors for k=5
    
    plot_filename_k3 = plot_admixture_with_sample_labels(admixture_k3, 3, colors_k3, population_code).replace(' ', '_')
    plot_filename_k5 = plot_admixture_with_sample_labels(admixture_k5, 5, colors_k5, population_code).replace(' ', '_')

    return [plot_filename_k3, plot_filename_k5]  # Return the filenames of the saved plots

# Main function to fetch and plot admixture data based on population_code or superpopulation
def main(input_value=None):
    # If no input_value is provided, default to a placeholder or fetch dynamically
    if input_value is None:
        input_value = "ABC"  # Placeholder, adjust as needed or remove if not desired
    # Determine if the input is a population code or a superpopulation
    is_population, is_superpopulation = check_input(input_value)

    if is_population:
        return main_population_code(input_value)
    elif is_superpopulation:
        return plot_admixture_for_superpopulation(input_value)
    else:
        print("Invalid input: Please enter a valid population code or superpopulation.")

# example tryout: 
#if __name__ == '__main__':
   # main('')



