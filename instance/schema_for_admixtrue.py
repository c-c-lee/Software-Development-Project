from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/farzadhamzawe/group_project bioinformatics/Software-Development-Project/instance/ArchGenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Population model
class Population(db.Model):
    population_code = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)

# Define the Admixture models
class Admixture_k3(db.Model):
    id = db.Column(db.String, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)
    Ancestry1 = db.Column(db.Float, nullable=False)
    Ancestry2 = db.Column(db.Float, nullable=False)
    Ancestry3 = db.Column(db.Float, nullable=False)

class Admixture_k5(db.Model):
    id = db.Column(db.String, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)
    Ancestry1 = db.Column(db.Float, nullable=False)
    Ancestry2 = db.Column(db.Float, nullable=False)
    Ancestry3 = db.Column(db.Float, nullable=False)
    Ancestry4 = db.Column(db.Float, nullable=False)
    Ancestry5 = db.Column(db.Float, nullable=False)

# Create the tables
with app.app_context():
    # If the population table does not exist, it will be created
    db.create_all()
