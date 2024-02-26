from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from src.analysis.flask_admixture import main_population_code, plot_admixture_for_superpopulation, check_input, get_population_code, get_superpopulation_code
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)

# Define routes
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/admixture', methods=['GET'])
def admixture():
    # This route should simply show the form.
    return render_template('admixture.html')

@app.route('/process_admixture', methods=['POST'])
def process_admixture():
    try:
        population_type = request.form['population_type']
        selected_items = request.form.getlist('selected_population')  # Correct variable name
        plot_filenames = []

        if population_type == 'superpopulation':
            for full_name in selected_items:  # Use 'selected_items' here
                superpopulation_code = get_superpopulation_code(full_name)
                if superpopulation_code:  # This 'if' block should be inside the 'for' loop
                    plot_files = plot_admixture_for_superpopulation(superpopulation_code)
                    plot_filenames.extend(plot_files)
                else:
                    print(f"Superpopulation code for '{full_name}' not found.")
        elif population_type == 'population':
            for full_name in selected_items:  # Use 'selected_items' here as well
                population_code = get_population_code(full_name)
                if population_code:
                    plot_files = main_population_code(population_code)
                    plot_filenames.extend(plot_files)
                else:
                    print(f"Population code for '{full_name}' not found.")

        return render_template('admixtureresults.html', plot_files=plot_filenames)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        app.logger.error(error_message)
        return error_message, 500

        

# Run the application
if __name__ == '__main__':
    app.run(debug=True)


#population analysis routes





#clustering routes






#if __name__ == '__main__':
    #app.run(debug=True)





