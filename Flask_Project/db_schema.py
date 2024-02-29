from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Define models
class Population(db.Model):
    population_code = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)

class SNP(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    chromosome = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    ref_allele = db.Column(db.String(255), nullable=False)
    alt_allele = db.Column(db.String(255), nullable=False)
    gene_name = db.Column(db.String(255), nullable=False)
    CLNALLELEID = db.Column(db.String(255), nullable=False)
    CLNDN = db.Column(db.String(255), nullable=False)
    CLNSIG = db.Column(db.String(255), nullable=False)

class AlleleFrequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    REF = db.Column(db.Float, nullable=False)
    ALT = db.Column(db.Float, nullable=False)
    position = db.Column(db.Integer, db.ForeignKey('snp.position'), nullable=False)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)

class GenotypeFrequency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Freq_HOM1 = db.Column(db.Float, nullable=False)
    Freq_HET = db.Column(db.Float, nullable=False)
    Freq_HOM2 = db.Column(db.Float, nullable=False)
    position = db.Column(db.Integer, db.ForeignKey('snp.position'), nullable=False)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)

class AdmixtureK3(db.Model):
    id = db.Column(db.String, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)
    Ancestry1 = db.Column(db.Float, nullable=False)
    Ancestry2 = db.Column(db.Float, nullable=False)
    Ancestry3 = db.Column(db.Float, nullable=False)

class AdmixtureK5(db.Model):
    id = db.Column(db.String, primary_key=True)
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)
    Ancestry1 = db.Column(db.Float, nullable=False)
    Ancestry2 = db.Column(db.Float, nullable=False)
    Ancestry3 = db.Column(db.Float, nullable=False)
    Ancestry4 = db.Column(db.Float, nullable=False)
    Ancestry5 = db.Column(db.Float, nullable=False)

class PCA(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added to serve as a unique identifier
    individual_id = db.Column(db.String(255), nullable=False)  # To store IndividualID
    pc1 = db.Column(db.Float, nullable=False)  # To store PC1 scores
    pc2 = db.Column(db.Float, nullable=False)  # To store PC2 scores
    population_code = db.Column(db.String(255), db.ForeignKey('population.population_code'), nullable=False)
    superpopulation = db.Column(db.String(255), nullable=False)
    
