import os
import sys
import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib.machinery import SourceFileLoader

# Add the directory containing the src directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(project_dir)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/instance/ArchGenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Construct the absolute path to db_schema.py
db_schema_path = '/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/database/db_schema.py'


# Import AdmixtureK3 and AdmixtureK5 from db_schema.py
db_schema = SourceFileLoader("db_schema", db_schema_path).load_module()
AdmixtureK3 = db_schema.AdmixtureK3
AdmixtureK5 = db_schema.AdmixtureK5

def populate_admixture_k3():
    with open('/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/tables/admixture_results/admixture_k3.tsv', 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            try:
                admixture_k3 = AdmixtureK3(
                    id=row['id'],
                    population_code=row['Population'],
                    superpopulation=row['SuperPopulation'],
                    Ancestry1=float(row['Ancestry1']),
                    Ancestry2=float(row['Ancestry2']),
                    Ancestry3=float(row['Ancestry3'])
                )
                db.session.add(admixture_k3)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Failed to add row {row['id']}: {e}")

def populate_admixture_k5():
    with open('/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/tables/admixture_results/admixture_k5.tsv', 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            try:
                admixture_k5 = AdmixtureK5(
                    id=row['id'],
                    population_code=row['Population'],
                    superpopulation=row['SuperPopulation'],
                    Ancestry1=float(row['Ancestry1']),
                    Ancestry2=float(row['Ancestry2']),
                    Ancestry3=float(row['Ancestry3']),
                    Ancestry4=float(row['Ancestry4']),
                    Ancestry5=float(row['Ancestry5'])
                )
                db.session.add(admixture_k5)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Failed to add row {row['id']}: {e}")

if __name__ == '__main__':
    with app.app_context():
        populate_admixture_k3()
        populate_admixture_k5()
