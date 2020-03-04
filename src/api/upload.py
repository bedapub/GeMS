"""
==============================================
upload.py: Import files into the GeMS Database
==============================================
__author__ = "Albert Kang"
__email__ = "swk30.cam@gmail.com"
__date__ = "29.10.2018"
__status__ = "In progress"

"""

import argparse
import os
import sys
from io import StringIO


from db_config import COLLECTION_NAME
from db_utils import db, create_collection, FIELD_CONSTRAINTS, INDEX_LIST
from gmtx_utils import parse_file, make_default_json, make_col_search_dict, make_batch_input
from gmtx_utils import make_api_default_json


def loadToMongo(jsonList):
	"""
	Upload logic: upsert on index
	
	:param jsonList: List<Dict>
	:return: VOID
	"""
	for geneset in jsonList:
		uniqueCondition = [{index: geneset[index]} for index in INDEX_LIST]
		db[COLLECTION_NAME].update({'$and': uniqueCondition}, geneset, upsert=True)
		
		
def api_insert(headers, rawList, params):
	"""
	Functional duplicate to ''main': inserts via REST-API
	
	Returns standard output error messages as a list of strings.
	
	Example:
		>>> from upload import api_insert
		
		>>> h = ['setName', 'desc', 'genes']
		>>> l = [['TIROSH_exhaution_marker', 'from TRIOSH table S14', 'CXCL13', 'TNFRSF1B', 'RGS2', 'TIGIT', 'CD27', 'TNFRSF9', 'SLA', 'ATP1B3', 'MYO7A', 'THADA', 'PARK7', 'EGR2', 'FDFT1', 'CRTAM', 'IFI16'], ['Speiser_EBV_DN', 'from Speiser_table S2', 'ACADSB', 'AFTPH', 'ARL1', 'ATP11C', 'CD160', 'CD244', 'CEP1MK', 'HIP1R', 'IER3', 'IGFBP4', 'INPP5B', 'INSL6', 'ITCH', 'KDSR', 'KLHL15', 'LRRC23']]
		>>> d = {'gf': 0, 'so': 'Roche', 'ti': 9606, 'us': 'kanga6'}
		
		>>> api_insert(h, l, d)
		['Error: CEP1MK (taxId  9606) is not valid.']
	
	:param headers: List<String>
	:param rawList: List<List<String>>
	:param params: Dict
	:return: List<String>
	"""
	assert all(s in params for s in ['gf', 'so', 'ti', 'us'])
	
	# Command-line error logging
	ogSys = sys.stdout
	s = StringIO()
	sys.stdout = s
	
	# Make search index for accepted and meta-tags
	geneFormat = params['gf']
	assert geneFormat in [0, 1, 2, 3]
	search_dict, hasCoeff, coeffType = make_col_search_dict(headers, geneFormat)
	
	# Find the constant elements of the geneset collection
	default_json = make_api_default_json(params, hasCoeff, coeffType)

	# Extract and merge
	mongo_input = make_batch_input(rawList, search_dict, default_json)
	
	# Load data
	loadToMongo(mongo_input)
	
	# Restore sys.stdout and get error messages
	sys.stdout = ogSys
	errorMsgs = s.getvalue().splitlines()
	
	return errorMsgs


def main():
	# Command line input
	parser = argparse.ArgumentParser()
	parser.add_argument('--fl', type=str, help='File location')
	parser.add_argument('--gf', type=int, help='Gene format: 0 for Native Gene Symbol, 1 for Native Entrez ID, 2 for Humanised Gene Symbol, 3 for Humanised Entrez ID')
	
	parser.add_argument('--so', type=str, help='Source: Name of the database(e.g. MSigDB) or Roche')
	parser.add_argument('--ti', type=int, help='NCBI Taxonomic ID')
	parser.add_argument('--us', type=str, help='User: "Public" or your Roche ID (e.g. "kanga6")')
	
	parser.add_argument('--st', type=str, default='', help='Subtype: database sub-category (e.g. C7)')
	parser.add_argument('--do', type=str, default='', help='Domain: functional meta-category (e.g. pathway)')
	

	# Input parameter constraints
	args = parser.parse_args()
	assert os.path.isfile(args.fl)
	assert args.gf in [0, 1, 2, 3]
	assert args.so is not None
	assert args.ti is not None
	assert args.us is not None

	# Parse file
	fileLoc = args.fl
	headers, rawList = parse_file(fileLoc)
	
	# Make search index for accepted and meta-tags
	geneFormat = args.gf
	search_dict, hasCoeff, coeffType = make_col_search_dict(headers, geneFormat)
	
	# Find the constant elements of the geneset collection
	default_json = make_default_json(args, hasCoeff, coeffType)

	# Extract and merge
	mongo_input = make_batch_input(rawList, search_dict, default_json)
	
	# Create collection
	if COLLECTION_NAME not in db.collection_names():
		create_collection(db, COLLECTION_NAME, FIELD_CONSTRAINTS, INDEX_LIST)
	
	# Load data
	loadToMongo(mongo_input)



if __name__ == '__main__':
	main()

