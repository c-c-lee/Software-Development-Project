
from db_schema import db, Population, Sample, SNP, AlleleFrequency, GenotypeFrequency
from flask_sqlalchemy import SQLAlchemy 
from db_schema import app

#test with db and make adjustments if needed

#queries for snp info route:

#retrieve snp info and clinical relevance based on snp id submitted by user
def get_AF_GF_from_id_list(snp_ids, populations):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            SNP.ref_allele,
            SNP.alt_allele,
            Population.population_code,
            AlleleFrequency.ref_allele_frequency,
            AlleleFrequency.alt_allele_frequency,
            GenotypeFrequency.Freq_HOM1,
            GenotypeFrequency.Freq_HET,
            GenotypeFrequency.Freq_HOM2
        ).select_from(SNP).join(
            AlleleFrequency, SNP.position == AlleleFrequency.position
        ).join(
            Population, AlleleFrequency.population_code == Population.population_code
        ).join(
            GenotypeFrequency, SNP.position == GenotypeFrequency.position
        ).filter(
            SNP.id.in_(snp_ids),
            Population.population_code.in_(populations)
        ).distinct().all()

    return result


def get_clinical_relevance_from_id_list(user_selected_snps):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            SNP.CLNALLELEID,
            SNP.CLNDN,
            SNP.CLNSIG
        ).filter(
            SNP.id.in_(user_selected_snps)
        ).all()

    return result

#retrieve snp info and clinical relevance based on genomic postions submitted by user
def query_genomic_region_and_population_AF_GF(genomic_region, populations):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            SNP.ref_allele,
            SNP.alt_allele,
            Population.population_code,
            AlleleFrequency.ref_allele_frequency,
            AlleleFrequency.alt_allele_frequency,
            GenotypeFrequency.Freq_HOM1,
            GenotypeFrequency.Freq_HET,
            GenotypeFrequency.Freq_HOM2
        ).select_from(SNP).join(
            AlleleFrequency, SNP.position == AlleleFrequency.position
        ).join(
            Population, AlleleFrequency.population_code == Population.population_code
        ).join(
            GenotypeFrequency, SNP.position == GenotypeFrequency.position
        ).filter(
            SNP.position.between(genomic_region[0][0], genomic_region[0][1]),
            Population.population_code.in_(populations)
        ).distinct().all()

    return result

#genomic_positions = [(100,200)]   e.g start, end position
#populations = ['GBR','IND', 'JPN']
   
#snp_info = query_genomic_region_and_population_AF_GF(genomic_regions, populations)  
#print(snp_info)

def get_clinical_relevance_from_genomic_region(genomic_region):
    with app.app_context():
        results = db.session.query(
            SNP.id,
            SNP.CLNALLELEID,
            SNP.CLNDN,
            SNP.CLNSIG
        ).filter(
            SNP.position.between(genomic_region[0][0], genomic_region[0][1])
        ).all()

    return results


#retrieve snp info and clinical relevance based on gene names list submitted by user

def get_AF_GF_from_gene_list(gene_names, populations):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            SNP.ref_allele,
            SNP.alt_allele,
            Population.population_code,
            AlleleFrequency.ref_allele_frequency,
            AlleleFrequency.alt_allele_frequency,
            GenotypeFrequency.Freq_HOM1,
            GenotypeFrequency.Freq_HET,
            GenotypeFrequency.Freq_HOM2
        ).select_from(SNP).join(
            AlleleFrequency, SNP.position == AlleleFrequency.position
        ).join(
            Population, AlleleFrequency.population_code == Population.population_code
        ).join(
            GenotypeFrequency, SNP.position == GenotypeFrequency.position
        ).filter(
            SNP.gene_name.in_(gene_names),
            Population.population_code.in_(populations)
        ).distinct().all()

    return result


def get_clinical_relevance_from_gene_list(gene_names):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            SNP.CLNALLELEID,
            SNP.CLNDN,
            SNP.CLNSIG
        ).filter(
            SNP.gene_name.in_(gene_names)
        ).all()

    return result



# Queries retrieve ref and alt allele frequencies for each pop per snp for matrix function in pop diff route:
# for each user input method(snp list, genomic postions and gene names)
def get_AF_for_matrix_multiple_pop_ids(snp_ids, populations):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            Population.population_code,
            AlleleFrequency.ref_allele_frequency,
            AlleleFrequency.alt_allele_frequency
        ).select_from(SNP).join(
        AlleleFrequency, SNP.position == AlleleFrequency.position
        ).join(
        Population, AlleleFrequency.population_code == Population.population_code
        ).filter(
        SNP.id.in_(snp_ids),
        Population.population_code.in_(populations)
        ).distinct().all()

    return result


def get_AF_for_matrix_multiple_pop_genes(gene_names, populations):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            Population.population_code,
            AlleleFrequency.ref_allele_frequency,
            AlleleFrequency.alt_allele_frequency
        ).select_from(SNP).join(
        AlleleFrequency, SNP.position == AlleleFrequency.position
        ).join(
        Population, AlleleFrequency.population_code == Population.population_code
        ).filter(
        SNP.gene_name.in_(gene_names),
        Population.population_code.in_(populations)
        ).distinct().all()

    return result


def get_AF_for_matrix_multiple_pop_genomic_region(genomic_region, populations):
    with app.app_context():
        result = db.session.query(
            SNP.id,
            Population.population_code,
            AlleleFrequency.ref_allele_frequency,
            AlleleFrequency.alt_allele_frequency,
        ).select_from(SNP).join(
            AlleleFrequency, SNP.position == AlleleFrequency.position
        ).join(
            Population, AlleleFrequency.population_code == Population.population_code
        ).filter(
            SNP.position.between(genomic_region[0][0], genomic_region[0][1]),
            Population.population_code.in_(populations)
        ).distinct().all()

    return result












