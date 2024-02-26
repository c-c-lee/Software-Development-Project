import os
import sys
import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# Add the directory containing db_schema.py to the Python path
sys.path.append('/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/database')

# Now you can import db_schema
from db_schema import db, AdmixtureK3, AdmixtureK5

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/instance/ArchGenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def populate_admixture(model, tsv_path):
    with app.app_context():
        # Clear previous data
        try:
            num_deleted = db.session.query(model).delete()
            db.session.commit()
            print(f"Cleared {num_deleted} existing records from {model.__name__}.")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error clearing data from {model.__name__}: {e}")
            return

        # Populate new data
        try:
            with open(tsv_path, 'r') as file:
                reader = csv.DictReader(file, delimiter='\t')
                for row in reader:
                    record = model(**{column: float(value) if column.startswith('Ancestry') else value 
                                      for column, value in row.items()})
                    db.session.add(record)
                db.session.commit()
                print(f"Inserted records into {model.__name__} successfully.")
        except (IOError, SQLAlchemyError) as e:
            db.session.rollback()
            print(f"Failed to populate {model.__name__}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Verify data insertion
        try:
            record_count = db.session.query(model).count()
            print(f"{record_count} records present in {model.__name__} after insertion.")
        except SQLAlchemyError as e:
            print(f"Error counting records in {model.__name__}: {e}")

if __name__ == '__main__':
    k3_tsv_path = '/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/tables/admixture_results/admixture_k3.tsv'
    k5_tsv_path = '/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/tables/admixture_results/admixture_k5.tsv'
    populate_admixture(AdmixtureK3, k3_tsv_path)
    populate_admixture(AdmixtureK5, k5_tsv_path)
