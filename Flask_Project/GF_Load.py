import gzip
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db_schema import GenotypeFrequency
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

def load_genotype_frequency_data(file_path, population_code):
    with gzip.open(file_path, 'rt') as file:
        # Assuming your TSV has a header and values are separated by tabs
        header = file.readline().strip().split('\t')

        for line in file:
            values = line.strip().split('\t')

            # Assuming columns in your TSV match the model attributes
            chromosome = values[0]
            position = int(values[1])

            # Replace 'nan' with None and then convert to float
            freq_hom1 = float(values[2]) if is_numeric(values[2]) else None
            freq_het = float(values[3]) if is_numeric(values[3]) else None
            freq_hom2 = float(values[4]) if is_numeric(values[4]) else None

            # Replace 'nan' with a default value (e.g., 0.0)
            freq_hom1 = freq_hom1 if freq_hom1 is not None and not math.isnan(freq_hom1) else 0.0
            freq_het = freq_het if freq_het is not None and not math.isnan(freq_het) else 0.0
            freq_hom2 = freq_hom2 if freq_hom2 is not None and not math.isnan(freq_hom2) else 0.0

            # Create an instance of GenotypeFrequency
            genotype_frequency = GenotypeFrequency(
                Freq_HOM1=freq_hom1,
                Freq_HET=freq_het,
                Freq_HOM2=freq_hom2,
                position=position,
                population_code=population_code
            )

            # Add the instance to the session
            db.session.add(genotype_frequency)

        # Commit changes to the database after processing the entire file
        db.session.commit()

        print(f"Loading for population {population_code} finished.")

if __name__ == '__main__':
    with app.app_context():
        # Provide the correct file paths and population codes for Genotype Frequency files
        gf_file_paths = [
            'Flask_Project/src/tables/Genotype_Frequency/ACB_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/ASW_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/BEB_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/CDX_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/CEU_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/CHB_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/CHS_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/CLM_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/ESN_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/FIN_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/GBR_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/GIH_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/GWD_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/IBS_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/ITU_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/JPT_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/KHV_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/LWK_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/MSL_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/MXL_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/PEL_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/PJL_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/PUR_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/SIB_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/STU_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/TSI_10_GF.tsv.gz',
            'Flask_Project/src/tables/Genotype_Frequency/YRI_10_GF.tsv.gz'
        ]

        gf_population_codes = ['ACB', 'ASW', 'BEB', 'CDX', 'CEU', 'CHB', 'CHS', 'CLM', 'ESN', 'FIN', 'GBR', 'GIH', 'GWD',
                               'IBS', 'ITU', 'JPT', 'KHV', 'LWK', 'MSL', 'MXL', 'PEL', 'PJL', 'PUR', 'SIB', 'STU', 'TSI', 'YRI']

        for file_path, population_code in zip(gf_file_paths, gf_population_codes):
            load_genotype_frequency_data(file_path, population_code)
