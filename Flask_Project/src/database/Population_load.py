# Flask_Project/src/database/Population_load.py

import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from db_schema import Population  # Import the Population model from db_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/cheaulee/Desktop/Software-Development-Project/Flask_Project/instance/ArchGenome.db'
db = SQLAlchemy(app)

def load_population_data():
    tsv_file_path = 'Flask_Project/src/tables/Population.tsv'
    data = pd.read_csv(tsv_file_path, sep='\t')

    with app.app_context():  # Create an application context
        for index, row in data.iterrows():
            population = Population(
                population_code=row['population'],
                name=row['population_name'],
                superpopulation=row['superpopulation']
            )

            try:
                db.session.add(population)
                db.session.commit()
            except IntegrityError:
                # Handle integrity errors (e.g., duplicate primary keys)
                db.session.rollback()

if __name__ == '__main__':
    load_population_data()