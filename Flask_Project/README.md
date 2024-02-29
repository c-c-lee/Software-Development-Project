# Software-Development-Project
# ArchGenome: Population Genetics Analysis Web Application

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
3. [Usage](#usage)
    - [Clustering Analysis](#clustering-analysis)
    - [Admixture Analysis](#admixture-analysis)
    - [Genetic Information Retrieval](#genetic-information-retrieval)
    - [Pairwise Population Genetic Differentiation](#pairwise-population-genetic-differentiation)
4. [Data Sources](#data-sources)
5. [Technologies Used](#technologies-used)
6. [Contributors](#contributors)
7. [Acknowledgements](#acknowledgements)
8. [License](#license)

---

## Introduction

ArchGenome is a web application developed by Team Arch as part of the MSC Bioinformatics Software Development Group Project 2024. The primary objective of ArchGenome is to facilitate population genetics analysis, focusing on human population genetics with an emphasis on samples from Siberia and the 1000 Genomes Project.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- [Python](https://www.python.org/) (version 3.8 or higher)
- [Virtualenv](https://pypi.org/project/virtualenv/)
- [Git](https://git-scm.com/)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/c-c-lee/Software-Development-Project.git
    cd Software-Development-Project
    ```

2. Create and activate a virtual environment:

    ```bash
    virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    python manage.py migrate
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

The application will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Usage

### Clustering Analysis

To perform clustering analysis using Principal Component Analysis (PCA):

1. Navigate to the "Clustering Analysis" section.
2. Choose the populations or superpopulations to include in the analysis.
3. Click "Submit" to generate PCA plots.

### Admixture Analysis

To conduct admixture analysis using ADMIXTURE or other selected algorithms:

1. Visit the "Admixture Analysis" section.
2. Select the desired populations or superpopulations.
3. Click "Submit" to visualize population structure.

### Genetic Information Retrieval

To retrieve genetic information for SNPs of interest:

1. Go to the "Population Information" section.
2. Select the desired population.
3. Choose to search by SNP IDs, genomic coordinates, or gene names.
5. Click "Submit" to obtain two tables. The first table presents allele and genotype frequencies. The second table presents clinical relevance information, in which the "CLNALLELEID" value can be copied onto the ClinVar website for users seeking the latest updates. 

### Pairwise Population Genetic Differentiation

To compute pairwise population genetic differentiation:

1. Navigate to the "Population Information" section.
2. Choose multiple populations.
3. Choose to search by SNP IDs, genomic coordinates, or gene names.
4. Click "Submit" to obtain two tables, population differentiation matrix, and download text file button. The first table presents allele and genotype frequencies. The second table presents clinical relevance information, in which the "CLNALLELEID" value can be copied onto the ClinVar website for users seeking the latest updates. 

---

## Data Sources

- Genetic data: Provided by collaborator, available on the module page on QMPlus.
- Annotation data: UCSC Genome Browser ([https://genome.ucsc.edu/](https://genome.ucsc.edu/)), Ensembl Genome Browser ([https://www.ensembl.org/](https://www.ensembl.org/)).
- Clinical relevance of SNPs: ClinVar ([https://www.ncbi.nlm.nih.gov/clinvar](https://www.ncbi.nlm.nih.gov/clinvar/)).

---

## Technologies Used

- FLASK: Web framework for backend development.
- SQLAlchemy and SQLite: Database management system.
- PCA, ADMIXTURE, Annovar: Algorithms and tools for clustering, admixture analysis, and data extraction.
- HTML, CSS, JavaScript: Frontend development.
- GitHub: Version control and collaborative development.

---
## Contributors

We would like to extend our gratitude to the following contributors for their valuable contributions to the ArchGenome project:

- [Cheau](https://github.com/c-c-lee)
- [Roxanna](https://github.com/Roxiiieee)
- [Farzad](https://github.com/farzhmz)
- [Siril](https://github.com/siril-qmul)
---
## Acknowledgements

We would like to express our gratitude to our collaborator for providing the genetic data and guidance throughout the project. Special thanks to the instructors for their support and valuable insights.

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to fork and modify as needed.
