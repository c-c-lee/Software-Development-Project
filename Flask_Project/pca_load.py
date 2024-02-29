import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_schema import db, PCA, Population

# Initialize Flask application
app = Flask(__name__)

# Used path of the project root path
print("ppppp")
project_root = 'C:/Users/ayush/OneDrive/Documents/Software-Development-Project'
# Absolute path to the database file
database_path = os.path.join(project_root, 'instance', 'ArchGenome.db')

# Ensure the instance directory exists
if not os.path.exists(os.path.dirname(database_path)):
    os.makedirs(os.path.dirname(database_path))

# Set the full URI for the database connection
db_uri = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Absolute path to the pca_scores.tsv file
tsv_file_path = os.path.join(project_root,'Flask_project','src', 'tables', 'pca_scores.tsv')
print(f"TSV file path: {tsv_file_path}")

def load_pca_data(filepath):
    # Read the data from the .tsv file into a pandas DataFrame
    pca_df = pd.read_csv(filepath, sep='\t')

    # Clear any existing data in the PCA table
    db.session.query(PCA).delete()

    # Iterate over the DataFrame and add each row to the database
    for index, row in pca_df.iterrows():
        pca_entry = PCA(
            individual_id=row['IndividualID'],
            pc1=row['PC1'],
            pc2=row['PC2'],
            population_code=row['Population'],
            superpopulation=row['Superpopulation']
        )
        db.session.add(pca_entry)

    # Commit the session to save the changes to the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Ensure that the database tables are created
        db.create_all()
        # Load the data into the database
        load_pca_data(tsv_file_path)
