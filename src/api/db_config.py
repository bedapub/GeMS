'''
=========================================
db_config.py: Database configuration file
=========================================
__author__ = "Albert Kang"
__email__ = "swk30.cam@gmail.com"
__date__ = "29.10.2018"
__status__ = "In progress"

'''
import os

MONGODB_USERNAME=os.environ['MONGODB_USERNAME']
MONGODB_PASSWORD=os.environ['MONGODB_PASSWORD']
MONGODB_HOST=os.environ['MONGODB_HOST']
MONGODB_PORT=os.environ['MONGODB_PORT']
MONGODB_DB=os.environ['MONGODB_DB']


# Collection names
COLLECTION_NAME = 'GeMS_genesets'
GENE_COL = 'ncbi_gene_info'
MAPPING_COL = 'ncbi_homologene'
