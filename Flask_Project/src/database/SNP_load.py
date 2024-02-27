import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Flask_Project.src.database.db_schema import SNP # Import the SNP model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Path/to/ArchGenome.db'
db = SQLAlchemy(app)

# Paths to your SNP files
file_paths = [
    'Flask_Project/src/tables/SNP/SNP_A.tsv.gz',
    'Flask_Project/src/tables/SNP/SNP_B.tsv.gz'
]

# Function to load data into the SNP table
def load_snp_data(file_path):\
    # Read SNP file into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t', compression='gzip')

    # Check if the file is SNP_A.tsv.gz and the first row is the same as the header, then skip the first row
    if 'SNP_A.tsv.gz' in file_path and (df.columns == df.iloc[0]).all():
        df = pd.read_csv(file_path, sep='\t', compression='gzip', skiprows=1)

    # Iterate through each row in the DataFrame and insert into the SNP table
    for index, row in df.iterrows():
        snp_entry = SNP(
            id=row['SNP_ID'],
            chromosome=row['Chromosome'],
            position=row['Start_Position'],
            ref_allele=row['Ref_Allele'],
            alt_allele=row['Alt_Allele'],
            gene_name=row['Gene_Name'],
            CLNALLELEID=row['CLNALLELEID'],
            CLNDN=row['CLNDN'],
            CLNSIG=row['CLNSIG']
        )
        db.session.add(snp_entry)

    # Commit the changes to the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        for file_path in file_paths:
            load_snp_data(file_path)