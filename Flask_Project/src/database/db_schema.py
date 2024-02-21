from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ArchGenome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models
class Population(db.Model):
    population_code = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)

class SNP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chromosome = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    ref_allele = db.Column(db.String(255), nullable=False)
    alt_allele = db.Column(db.String(255), nullable=False)
    gene_name = db.Column(db.String(255), nullable=False)
    CLNALLELEID = db.Column(db.String(255), nullable=False)
    CLNDN = db.Column(db.String(255), nullable=False)
    CLNSIG = db.Column(db.String(255), nullable=False)

class AlleleFrequency(db.Model):
    allele_frequency = db.Column(db.Float, primary_key=True)
    position = db.Column(db.Integer, db.ForeignKey('snp.position'), nullable=False)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    snp_id = db.Column(db.Integer, db.ForeignKey('snp.id'), nullable=False)

class GenotypeFrequency(db.Model):
    genotype_frequency = db.Column(db.Float, primary_key=True)
    position = db.Column(db.Integer, db.ForeignKey('snp.position'), nullable=False)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    snp_id = db.Column(db.Integer, db.ForeignKey('snp.id'), nullable=False)

class Admixture(db.Model):
    results = db.Column(db.Float, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    superpopulation = db.Column(db.String(255), db.ForeignKey('population.superpopulation'), nullable=False)

class PCA(db.Model):
    results = db.Column(db.Float, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    superpopulation = db.Column(db.String(255), db.ForeignKey('population.superpopulation'), nullable=False)
    
with app.app_context():
    db.create_all()