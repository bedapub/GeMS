"""
===============================================================
cellmarker_to_gmtx.py: CellMarker genesets -> .gmtx file format
===============================================================
__contact__ = 'swk30.cam@gmail.com'
__date__ = '19.11.2018'
__status__ = 'In progress'

"""

import argparse
import os


META_KEYS = ['speciesType', 'tissueType2', 'cancerType', 
				'cellType', 'markerResource', 'PMID', 'Company']
GENES_KEY = 'geneID'
GENESET_ID_KEY = 'cellName3'
ORGANISM_KEY = 'speciesType'


def getGeneList(s):
	"""
	Process a string of Entrez GeneIds separated by commas and
	additionally filter non-numeric elements.
	
	:param s: String 
	:return: List<String>
	"""
	s = s.replace('[', '').replace(']', '')
	rawGeneList = s.split(', ')
	geneList = [x for x in rawGeneList if x.isnumeric()]
	return geneList


def main():
	# Command-line input
	parser = argparse.ArgumentParser()
	parser.add_argument('--f', type=str, help='File location')
	args = parser.parse_args()
	assert os.path.isfile(args.f)
	inFileLoc = args.f
	outFileLoc = '.'.join(inFileLoc.split('.')[:-1]) + '.gmtx'

	# Load file onto 'rawList'
	rawList = []
	with open(inFileLoc, 'r') as f:
		for l in f:
			splitL = l.rstrip().split('\t')
			rawList.append(splitL)
	rawColHeaders, rawList = rawList[0], rawList[1:]
	assert all(len(lst) == len(rawColHeaders) for lst in rawList)
	
	# Make header index
	headerIndexLookup = {rawColHeaders[i]: i for i in range(len(rawColHeaders))}
	metaIndexes = [headerIndexLookup[s] for s in META_KEYS]
	idIndex = headerIndexLookup[GENESET_ID_KEY]
	geneIndex = headerIndexLookup[GENES_KEY]
	
	# Counter for GENESET_ID_KEY - enforce uniqueness
	idCounter = dict()
	gmtxHeaders = ['setName'] + META_KEYS + ['genes']
	rawWriteOut = []
	
	for l in rawList:
		_meta = [l[i] for i in metaIndexes]
		_id = l[idIndex]
		_gene = getGeneList(l[geneIndex])
		
		# If no gene membership info. available => skip
		if len(_gene) == 0:
			 continue
		
		# Make unique id
		if _id not in idCounter:
			idCounter[_id] = 1
		else:
			idCounter[_id] += 1
			_id = _id + ' ' + str(idCounter[_id])
		
		# Concatenate
		outList = [_id] + _meta + _gene
		rawWriteOut.append(outList)

	# Separate by organism
	orgIndex = gmtxHeaders.index(ORGANISM_KEY)
	orgSepGeneDict = dict()
	for l in rawWriteOut:
		organism = l[orgIndex]
		if organism not in orgSepGeneDict:
			orgSepGeneDict[organism] = []
		orgSepGeneDict[organism].append(l)
	
	# Write out
	for k, v in orgSepGeneDict.items():
		newOutfile = k + '_' + outFileLoc
		with open(newOutfile, 'w', encoding='utf-8') as g:
			g.write('\t'.join(gmtxHeaders) + '\n')
			for x in v:
				g.write('\t'.join(x) + '\n')
	

if __name__ == '__main__':
	main()