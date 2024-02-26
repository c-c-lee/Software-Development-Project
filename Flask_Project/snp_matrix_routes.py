#draft code
from flask import Flask, render_template, request, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from src.analysis.matrix_function import calculate_pairwise_fst
from src.database.db_schema import db, app, SNP, Sample, AlleleFrequency, GenotypeFrequency
from src.database.db_sql_queries import get_AF_for_matrix_multiple_pop_genes, get_AF_for_matrix_multiple_pop_genomic_region, get_AF_for_matrix_multiple_pop_ids, get_AF_GF_from_id_list, get_AF_GF_from_gene_list, query_genomic_region_and_population_AF_GF, get_clinical_relevance_from_id_list, get_clinical_relevance_from_gene_list, get_clinical_relevance_from_genomic_region
import base64
from io import BytesIO
#homepage

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

#snp routes:

@app.route('/population', methods = ['GET'])
def populations():
    # shows form
    return render_template('snp.html')

@app.route('/retrieve_snp_info', methods = ['GET','POST'])
def retrieve_snp_info():
    # route retrieves POST request for snp ids and population selections
    if request.method == 'POST':
        user_input_type = request.form.get('input_type') #retrieve input type
        user_input_value = request.form.getlist('input_value').split(',') #get snp ids

        # Retrieve selected populations as a list
        selected_population = request.form.get('selected_population') # get population from user form

        # Handle different input types
        if user_input_type == 'snp_id':
            SNP_freq = get_AF_GF_from_id_list(user_input_value, selected_population)
            Clinical_relevance = get_clinical_relevance_from_id_list(user_input_value)
            
        elif user_input_type == 'genomic_coordinates':
            #convert user input into tuples (e.g user input = 100,200 then genomic postion = [(100,200)])
            genomic_positions = [tuple(map(int, user_input_value))]
            SNP_freq = query_genomic_region_and_population_AF_GF(genomic_positions, selected_population)
            Clinical_relevance = get_clinical_relevance_from_genomic_region(genomic_positions)
        
        elif user_input_type == 'gene_names':
            SNP_freq = get_AF_GF_from_gene_list(user_input_value, selected_population)
            Clinical_relevance = get_clinical_relevance_from_gene_list(user_input_value)
        

        # Render the result template with the data retrieved from the queries if POST request
        return render_template('snpresults.html', SNP_freq=SNP_freq, Clinical_relevance= Clinical_relevance )

    # Render the initial form if it's a GET request
    return render_template('snp.html')





#population differentation routes


@app.route('/population_differentation', methods = ['GET'])
def population_differentation():
    #shows form
    return render_template('popdiff.html')

@app.route('/process_matrix_downloadlink', methods = ['GET','POST'])
def pd_matrix():
    if request.method == 'POST':
        user_input_type = request.form.get('input_type') #retrieve input type
        user_input_value = request.form.getlist('input_value').split(',') #get snp ids
        #Retrieve selected populations as a list
        selected_populations = request.form.getlist('selected_populations')# get population(S) from user form  ?

        if user_input_type == 'snp_id':
            query = get_AF_for_matrix_multiple_pop_ids(user_input_value, selected_populations) 
            matrix, image, filepath = calculate_pairwise_fst(query) #function outputs matrix and filepath where txt file is
        elif user_input_type == 'genomic_coordinates':
            #convert user input into tuples (e.g user input = 100,200 then genomic postion = [(100,200)])
            genomic_positions = [tuple(map(int, user_input_value))]
            query = get_AF_for_matrix_multiple_pop_genomic_region(genomic_positions, selected_populations)
            matrix, image, filepath = calculate_pairwise_fst(query)
        elif user_input_type == 'gene_names':
            query = get_AF_for_matrix_multiple_pop_genes(user_input_value, selected_populations)
            matrix, image, filepath = calculate_pairwise_fst(query)

        download_url = url_for('download_fst_matrix', filepath=filepath)
        
        return render_template('popdiffresults.html', image=image, download_url=download_url) 


    return render_template('popdiff.html')
        


@app.route('/download_fst_matrix', methods=['GET'])
def download_fst_matrix():
    filepath = request.args.get('filepath')

    if filepath:
        return send_file(filepath, as_attachment=True, download_name="pairwise_fst_matrix.txt")
    else:
        return "File not found."
