# libraries imported here
from src.analysis.pca import load_pca_data, main
import matplotlib
import matplotlib.pyplot as plt

db_path = "Software-Development-Project/instance/ArchGenome.db"
app = Flask(__name__)

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