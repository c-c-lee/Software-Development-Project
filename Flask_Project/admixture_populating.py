# Import necessary modules
import csv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(_name_)

# Configure the SQLAlchemy database URI, defaulting to a SQLite database named ArchGenome.db
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///ArchGenome.db')

# Disable the Flask-SQLAlchemy event system to improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Import the table models from db_schema.py after initializing SQLAlchemy to avoid circular imports
from db_schema import AdmixtureK3, AdmixtureK5

# Define a function to populate a database table from a TSV (Tab-Separated Values) file
def populate_admixture_table(file_path, table_model):
    # Open the TSV file for reading
    with open(file_path, 'r') as file:
        # Create a CSV reader object to read the file with a tab delimiter
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip the header row
        
        # Iterate over each row in the TSV file
        for row in reader:
            # Create an instance of the table model with data from the current row
            entry = table_model(
                id=row[0],
                population_code=row[1],
                super_population=row[2],
                Ancestry1=float(row[3]),
                Ancestry2=float(row[4]),
                Ancestry3=float(row[5]),
                Ancestry4=float(row[6]) if len(row) > 6 else None,  # Handle optional fields
                Ancestry5=float(row[7]) if len(row) > 7 else None
            )
            # Merge the new or existing entry into the session
            db.session.merge(entry)
            
    # Try to commit changes to the database
    try:
        db.session.commit()
        print(f"Entries from {file_path} successfully inserted into {table_model._name_}.")
    except Exception as e:  # Catch any exceptions during commit
        db.session.rollback()  # Roll back the session in case of an exception
        print(f"Error inserting entries from {file_path} into {table_model._name_}: {str(e)}")

# Main block to run the script
if _name_ == '_main_':
    # Ensure the Flask app context is available for SQLAlchemy operations
    with app.app_context():
        # Define the base directory for the TSV files
        base_dir = '/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/tables/admixture_results'
        
        # Define the file path for the AdmixtureK3 table data and populate the table
        admixture_k3_file = os.path.join(base_dir, 'admixture_k3.tsv')
        populate_admixture_table(admixture_k3_file, AdmixtureK3)
        
        # Define the file path for the AdmixtureK5 table data and populate the table
        admixture_k5_file = os.path.join(base_dir, 'admixture_k5.tsv')
        populate_admixture_table(admixture_k5_file, AdmixtureK5)