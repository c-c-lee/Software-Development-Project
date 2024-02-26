from flask import Flask, request, render_template, send_from_directory
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sys.path.append('C:/Users/roxan/OneDrive/Documents/GitHub/Software-Development-Project')

from src.analysis.pca import load_pca_data, plot_pca

#import sql queries and other funtions from relevant directories

app = Flask(__name__)


# Define routes for backend here: 
@app.route('/')
def index():
    return render_template('clustering.html')  # Assuming your form HTML file is named select_form.html

@app.route('/submit', methods=['POST'])
def submit():
    # Extract form data
    population_type = request.form['population_type']
    selected_population = request.form['selected_population']

    # Load PCA data and generate plot
    filepath = 'Flask_Project/src/tables/pca_scores.tsv'
    pca_data = load_pca_data(filepath)
    
    # Define output path for the plot
    output_filename = f"pca_plot_{population_type}_{selected_population}.png"
    output_path = os.path.join('static', output_filename)  # Make sure 'static' directory exists

    # Generate plot
    plot_pca(pca_data, selected_population, population_type, output_path)

    # Render template to display results
    # Pass necessary data to the template, including the path to the generated plot image
    return render_template('clusteringresults.html', 
                           population_type=population_type, 
                           selected_population=selected_population, 
                           image_file=output_filename)

if __name__ == '__main__':
    app.run(debug=True)


#homepage route

#@app.route("/")
#@app.route("/home")
#def home():
    #return render_template("index.html")

#admixture routes 

#@app.route("")



#population analysis routes





#clustering routes






#if __name__ == '__main__':
    #app.run(debug=True)





