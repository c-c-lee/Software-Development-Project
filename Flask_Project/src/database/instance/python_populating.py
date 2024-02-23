import os
import sys
import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Set the path to the directory ABOVE 'src'
project_dir = '/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project'
sys.path.append(project_dir + '/src')  # Ensure the 'src' directory is in the path

from database.db_schema import AdmixtureK3, AdmixtureK5

app = Flask(__name__)
# Corrected the database URI to point to the correct database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_dir, 'src/instance/ArchGenome.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def populate_admixture_k3():
    with open(os.path.join(project_dir, 'src/tables/admixture_results/admixture_k3.tsv'), 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            try:
                admixture_k3 = AdmixtureK3(
                    id=row['id'],
                    population_code=row['Population'],
                    super_population=row['Super_Population'],
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
    with open(os.path.join(project_dir, 'src/tables/admixture_results/admixture_k5.tsv'), 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            try:
                admixture_k5 = AdmixtureK5(
                    id=row['id'],
                    population_code=row['Population'],
                    super_population=row['Super_Population'],
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