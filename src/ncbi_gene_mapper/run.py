'''
run.py - Load gene mappings into a MongoDB collection
'''

import os

MONGODB_USERNAME=os.environ['MONGODB_USERNAME']
MONGODB_PASSWORD=os.environ['MONGODB_PASSWORD']
MONGODB_HOST=os.environ['MONGODB_HOST']
MONGODB_PORT=os.environ['MONGODB_PORT']
MONGODB_DB=os.environ['MONGODB_DB']

GENE_COL = 'GeMS_gene_info'
MAPPING_COL = 'GeMS_homologene_map'


# File Configuration

GENE_INFO_FILE = 'gene_info.txt'
HOMOLOGENE_FILE = 'homologene.data'


# Helper Functions

def mapIdToSymbol(fileLoc):
	"""
	Outputs a dictionary with key, value:
		KEY: <Int> - Gene ID
		VALUE: Dict with keys:
			- taxId: <Int>
			- geneSymbol: <String>
	
	:param fileLoc: String - File location of NCBI Entrez Gene ID information
	:return infoDict: Dict
	"""
	# Define column indexes
	taxIdCol = 0
	geneIdCol = 1
	geneSymbolCol = 2
	synonymCol = 4
	
	# Initialise data store
	infoDict = dict()
	
	# Read file and store info
	with open(fileLoc, 'r') as f:
		f.readline()
		for l in f:
			l = l.split('\t')
			geneId = int(l[geneIdCol])
			assert geneId not in infoDict
			
			geneJson = {'taxId': int(l[taxIdCol]),
						'Symbol': l[geneSymbolCol]}
			infoDict[geneId] = geneJson
			
			# Synonyms
			rawSynonyms = l[synonymCol]
			if rawSynonyms != '-':
				infoDict[geneId]['Synonyms'] = rawSynonyms.split('|')

	return infoDict


def homologyMapping(fileLoc):
	"""
	Outputs a dictionary with key, value:
		KEY: <Int> - HomoloGene ID
		VALUE: List<Dict> - Dict with keys:
			- taxId: <Int>
			- geneId: <Int>
		
	:param fileLoc: String - File location of HomoloGene data
	:return orthoDict: Dict<List>
	"""
	# Define column indexes
	homIdCol = 0
	taxIdCol = 1
	geneIdCol = 2
	
	# Initialise data store
	orthoDict = dict()
	
	# Read file and store info
	with open(fileLoc, 'r') as f:
		for l in f:
			l = l.split('\t')
			homId = int(l[homIdCol])
			taxId = int(l[taxIdCol])
			geneId = int(l[geneIdCol])
			
			member = {'taxId': taxId, 'geneId': geneId}
			if homId not in orthoDict:
				orthoDict[homId] = list()
			orthoDict[homId].append(member)
			
	return orthoDict


def main():
	# File scrape
	print('Scraping files...')
	id2sym = mapIdToSymbol(GENE_INFO_FILE)
	homMap = homologyMapping(HOMOLOGENE_FILE)
	
	# Format (and merge raw data dictionaries)
	print('Formatting into JSON objects...')
	geneInfoJSON = [{'geneId': k, **v} for k, v in id2sym.items()]
	homInfoJSON = [{'homId': k, 'members': v} for k, v in homMap.items()]
	
	# Upload to Mongo collection
	print('Uploading to MongoDB...')
	db[GENE_COL].drop()
	db.create_collection(GENE_COL)
	db[GENE_COL].insert_many(geneInfoJSON)
	
	db[MAPPING_COL].drop()
	db.create_collection(MAPPING_COL)
	db[MAPPING_COL].insert_many(homInfoJSON)


if __name__ == '__main__':
	main()
