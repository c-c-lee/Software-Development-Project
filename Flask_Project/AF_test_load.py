import gzip
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_schema import AlleleFrequency
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/ArchGenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def load_allele_frequency_data(file_path, population_code):
    with gzip.open(file_path, 'rt') as file:
        header = file.readline().strip().split('\t')

        for line in file:
            values = line.strip().split('\t')

            # Columna in TSV match the model attributes
            chromosome = values[0]
            position = int(values[1])
            
            # Replace 'nan' with None and then convert to float
            ref = float(values[2]) if is_numeric(values[2]) else None
            alt = float(values[3]) if is_numeric(values[3]) else None

            # Default values input here (e.g., 0.0)
            ref = ref if ref is not None and not math.isnan(ref) else 0.0
            alt = alt if alt is not None and not math.isnan(alt) else 0.0

            # Create an instance of AlleleFrequency
            allele_frequency = AlleleFrequency(
                REF=ref,
                ALT=alt,
                position=position,
                population_code=population_code
            )

            # Add the instance to the session
            db.session.add(allele_frequency)

        # Commit changes to the database after processing the entire file
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Provide the correct file path and population code i.e. ASW
        file_path = '/tables/Allele_Frequency/ASW_AF.tsv.gz'
        population_code = 'ASW'

        load_allele_frequency_data(file_path, population_code)