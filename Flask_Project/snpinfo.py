import sqlite3
import os, sys
from db_schema import *


# Path to your SQLite database
def get_snp_info(snp_id, population_code):
    """Retrieve genotype and allele frequencies for a given snp and population."""
    print("aaaaaa")
    snp = SNP.query.filter_by(id=snp_id).first()

    if not snp:
        return None, None  # SNP not found

    genotype_freq = GenotypeFrequency.query.filter_by(position=snp.position, population_code=population_code).first()
    allele_freq = AlleleFrequency.query.filter_by(position=snp.position, population_code=population_code).first()

    return (genotype_freq.Freq_HOM1, genotype_freq.Freq_HET, genotype_freq.Freq_HOM2) if genotype_freq else None, \
           (allele_freq.REF, allele_freq.ALT) if allele_freq else None

# def get_clinical_relevance(snp_id):
#     """Retrieve clinical relevance information for a given snp."""
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Adjusted query to fetch clinical relevance details from the SNP table
#     cursor.execute('''
#         SELECT CLNALLELEID, CLNDN, CLNSIG FROM snp
#         WHERE id = ?
#     ''', (snp_id,))
#     clinical_info = cursor.fetchall()

# def get_snps_by_coordinates(start, end):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT id FROM snp
#         WHERE position BETWEEN ? AND ?;
#     ''', (start, end))
#     snp_ids = cursor.fetchall()
#     conn.close()
#     return [snp_id[0] for snp_id in snp_ids]  # Unpack the tuple results into a list of SNP IDs

# def get_snps_by_gene_name(gene_name):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT id FROM snp
#         WHERE gene_name = ?;
#     ''', (gene_name,))
#     snp_ids = cursor.fetchall()
#     conn.close()
#     return [snp_id[0] for snp_id in snp_ids]  # Convert tuple results to a list of SNP IDs



#     conn.close()
#     return clinical_info

# Test SNP ID: 1:10399:C:A

#genotype_freq, allele_freq = get_snp_info('1:10399:C:A', 'SIB')
# clinical_info = get_clinical_relevance('1:10399:C:A')
#print("1:10399:C:A - Genotype Frequencies:", genotype_freq)
#print("1:10399:C:A - Allele Frequencies:", allele_freq)
# print("1:10399:C:A - Clinical Relevance:", clinical_info)

# Test SNP ID: rs2802011;1:89973745:G:A (adjust if necessary to match database format)
# genotype_freq, allele_freq = get_snp_info('rs2802011;1:89973745:G:A', 'Population_Code')
# clinical_info = get_clinical_relevance('rs2802011;1:89973745:G:A')
# print("rs2802011;1:89973745:G:A - Genotype Frequencies:", genotype_freq)
# print("rs2802011;1:89973745:G:A - Allele Frequencies:", allele_freq)
# print("rs2802011;1:89973745:G:A - Clinical Relevance:", clinical_info)
