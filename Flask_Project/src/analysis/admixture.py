import sys
sys.path.append('/Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/src/database')

from db_schema import db, AdmixtureK3, AdmixtureK5
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/Flask_Project/instance/ArchGenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


from db_schema import db, AdmixtureK3, AdmixtureK5

def extract_rows(population_code):
    with app.app_context():
        # Query for AdmixtureK3
        admixture_k3_rows = AdmixtureK3.query.filter_by(population_code=population_code).limit(10).all()
        for row in admixture_k3_rows:
            print(row.id, row.population_code, row.superpopulation, row.Ancestry1, row.Ancestry2, row.Ancestry3)
        
        # Query for AdmixtureK5
        admixture_k5_rows = AdmixtureK5.query.filter_by(population_code=population_code).limit(10).all()
        for row in admixture_k5_rows:
            print(row.id, row.population_code, row.superpopulation, row.Ancestry1, row.Ancestry2, row.Ancestry3, row.Ancestry4, row.Ancestry5)

if __name__ == '__main__':
    extract_rows('ASW')