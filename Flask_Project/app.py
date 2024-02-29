# libraries imported here
from flask_sqlalchemy import SQLAlchemy
from pca import load_pca_data, main
import matplotlib
import matplotlib.pyplot as plt
import os
from flask import Flask, request, render_template, url_for, send_file

from flask_admixture import main_population_code, plot_admixture_for_superpopulation, check_input, get_population_code, get_superpopulation_code
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from matrix_function import calculate_pairwise_fst
from db_schema import db, Population, Sample, SNP, AlleleFrequency, GenotypeFrequency

import SNPID_PD
import Genomic_Coordinates_PD
import Gene_Name_PD

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ArchGenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():

    return render_template("index.html")

@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")


# Clustering analysis route

@app.route('/clustering', methods=['GET'])
def clustering():
    # This route should simply show the form.
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

@app.route('/admixture', methods=['GET'])
def admixture():
    # This route should simply show the form.
    return render_template('admixture.html')

@app.route('/process_admixture', methods=['POST'])
def process_admixture():
    try:
        population_type = request.form['population_type']
        selected_items = request.form.getlist('selected_population')  
        plot_filenames = []

        if population_type == 'superpopulation':
            for full_name in selected_items:  
                superpopulation_code = get_superpopulation_code(full_name)
                if superpopulation_code:  # This 'if' block should be inside the 'for' loop
                    plot_files = plot_admixture_for_superpopulation(superpopulation_code)
                    plot_filenames.extend(plot_files)
                else:
                    print(f"Superpopulation code for '{full_name}' not found.")
        elif population_type == 'population':
            for full_name in selected_items:  
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

    
# Population Differentiation route

@app.route('/popdiff', methods=['GET'])
def popdiff():
    # This route should simply show the form.
    return render_template('popdiff.html')

@app.route('/process_popdiff', methods=['POST'])
def process_popdiff():
    try:
        user_input_type = request.form.get('input_type')  # Retrieve input type

        selected_populations = request.form.getlist('selected_population')
        population_codes = Population.query.filter(Population.name.in_(selected_populations)).with_entities(Population.population_code).all()
        population_codes = [code[0] for code in population_codes]

        if user_input_type == 'snp_id':

            user_input_values = request.form.getlist('input_value') 
            input_string = user_input_values[0]
            snp_ids = input_string.split(',')

            # population_codes = ["JPT", "GBR", "MXL"]
            # snp_ids = ["rs2802011;1:89973745:G:A", "1:10399:C:A"]
            fst_results = SNPID_PD.calculate_fst(population_codes, snp_ids)
            df_fst = SNPID_PD.save_fst_results_to_dataframe(fst_results)
            SNPID_PD.save_dataframe_to_file(df_fst, 'fst_results.txt')

            filenames_lst = []
            for snp_id in snp_ids:
                filenames = SNPID_PD.create_fst_heatmap(df_fst[df_fst['SNP_ID'] == snp_id], snp_id)
                filenames_lst.append(filenames)
            
            
            return render_template('popdiffresults.html',filenames_lst = filenames_lst, c = 0)

        elif user_input_type == 'genomic_coordinates':

            user_input_values = request.form.getlist('input_value')  # Retrieve input values as a list
            input_string = user_input_values[0]
            snp_ids = input_string.split(',')

            snp_ids = input_string.split(',')
            positions = []
            for i in snp_ids:
                positions.append(int(i))

            # population_codes = ["JPT", "GBR", "MXL"]
            # positions = [10437, 10438]  
            
            fst_results = Genomic_Coordinates_PD.calculate_fst(population_codes, positions)
            df_fst = Genomic_Coordinates_PD.save_fst_results_to_dataframe(fst_results)
            df_fst.to_csv('fst_results_positions.txt', sep='\t', index=False)

            filenames_lst = []
            for position in positions:
                filenames = Genomic_Coordinates_PD.plot_heatmap(df_fst, position)
                filenames_lst.append(filenames)

            return render_template('popdiffresults.html',filenames_lst = filenames_lst, c = 1)

        elif user_input_type == 'gene_names':

            user_input_values = request.form.getlist('input_value') 
            input_string = user_input_values[0]
            gene_names = input_string.split(',')

            # population_codes = ["JPT", "GBR", "MXL"]
            gene_names = ["FH", "OPN3"] 
            fst_results = Gene_Name_PD.calculate_fst(population_codes, gene_names)

            df_fst = Gene_Name_PD.save_fst_results_to_dataframe(fst_results)

            df_fst.to_csv('gene_fst_results.txt', sep='\t', index=False)

            filenames_lst = []
            for gene_name in gene_names:
                filenames = Gene_Name_PD.plot_heatmap(df_fst, gene_name)
                filenames_lst.append(filenames)
            return render_template('popdiffresults.html',filenames_lst = filenames_lst, c = 2)

    except Exception as e:
        error_message = f"An error occurred: {e}"
        app.logger.error(error_message)
        return "Error"


@app.route('/download_fst_results')
def download_fst_matrixx():
    filepath = "fst_results.txt"
    return send_file(filepath, as_attachment=True)

@app.route('/download_fst_results_positions')
def download_fst_matrix():
    filepath = "fst_results_positions.txt"
    return send_file(filepath, as_attachment=True)

@app.route('/download_genes_fst_results')
def download_fst_matrixxx():
    filepath = "gene_fst_results.txt"
    return send_file(filepath, as_attachment=True)

# SNP Matrix route
@app.route('/snp', methods=['GET'])
    # This route should simply show the form.
def snp_information():
    return render_template('snp.html')

@app.route('/snp_processing', methods=['POST'])
def snp_processing():
    try:
        population_type = request.form['population_type']
        selected_population = request.form['selected_population']
        input_type = request.form['input_type']
        input_value = request.form['input_value']

        print(population_type, selected_population, input_type, input_value)

        if(input_type == "snp_id"):
            snp = SNP.query.filter_by(id=input_value).first()
            population = Population.query.filter_by(name=selected_population).first()
            if not snp or not population:
                return None, None
            allele_frequency = AlleleFrequency.query.filter_by(position=snp.position, population_code=population.population_code).first()
            genotype_frequency = GenotypeFrequency.query.filter_by(position=snp.position, population_code=population.population_code).first()

            return render_template("snpresults.html", snp = snp, selected_population = selected_population, allele_frequency = allele_frequency, genotype_frequency = genotype_frequency)
        
        elif input_type == "genomic_coordinates":
            values = input_value.split(',')
            snp_ids = SNP.query.filter(SNP.position.between(values[0], values[1])).with_entities(SNP.id).all()
            population = Population.query.filter_by(name=selected_population).first()
            
            results = []
            for snp_id in snp_ids:
                snp = SNP.query.filter_by(id=snp_id[0] ).first()
                allele_frequency = AlleleFrequency.query.filter_by(position=snp.position, population_code=population.population_code).first()
                genotype_frequency = GenotypeFrequency.query.filter_by(position=snp.position, population_code=population.population_code).first()

                results.append({'snp': snp, 'allele_frequency': allele_frequency, 'genotype_frequency': genotype_frequency})
            return render_template("snp_genomic_coordinates.html", results=results, selected_population=selected_population)
        
        elif input_type == "gene_names":
            snp_ids = SNP.query.filter_by(gene_name=input_value).with_entities(SNP.id).all()
            population = Population.query.filter_by(name=selected_population).first()

            results = []
            for snp_id in snp_ids:
                snp = SNP.query.filter_by(id=snp_id[0] ).first()
                allele_frequency = AlleleFrequency.query.filter_by(position=snp.position, population_code=population.population_code).first()
                genotype_frequency = GenotypeFrequency.query.filter_by(position=snp.position, population_code=population.population_code).first()

                results.append({'snp': snp, 'allele_frequency': allele_frequency, 'genotype_frequency': genotype_frequency})
            return render_template("snp_genes.html", results=results, selected_population=selected_population)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        app.logger.error(error_message)
        return error_message, 500
    

# Code to make the app run, this stays at the bottom
if __name__ == '__main__':
    app.run()