# libraries imported here
from src.analysis.pca import load_pca_data, main
import matplotlib
import matplotlib.pyplot as plt
import os
from flask import Flask, request, render_template, url_for
    
from src.analysis.flask_admixture import main_population_code, plot_admixture_for_superpopulation, check_input, get_population_code, get_superpopulation_code
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Path to the database file
db_path = 'Software-Development-Project/instance/Archgenome.db'

app = Flask(__name__, static_url_path='/static')

# Clustering analysis route

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/clustering', methods=['GET'])
def clustering():
    return render_template('clustering.html')

@app.route('/process_clustering', methods=['POST'])
def process_clustering():
    try:
        population_type = request.form['population_type']
        selected_population = request.form['selected_population']

        selection_type = 'Superpopulation' if population_type == 'superopulation' else 'Population'

        output_filename = main(selected_population, selection_type)

        return render_template('clusteringresults.html', plot_files= output_filename)
    
    except Exception as e:
        return f"An error occured: {e}", 500

# Admixture route
    


# Population Differentiation route
    

# SNP Matrix route
    

    

# Code to make the app run, this stays at the bottom
if __name__ == '__main__':
    app.run(debug=True)