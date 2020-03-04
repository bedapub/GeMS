"""
==========================================================
gmtx_utils.py: Utils for data manipulation with GMTX files
==========================================================
__author__ = "Albert Kang"
__email__ = "swk30.cam@gmail.com"
__date__ = "29.10.2018"
__status__ = "In progress"

"""

import datetime

from db_utils import ACCEPTED_HEADERS, ACCEPTED_COEFF_TYPE
from map_utils import getGeneArray


def parse_file(file):
	"""
	Parse .GMTX tab-delimited file
	
	:param file: String
	:return headerList: List<String>
	:return rawDataList: List<String>
	"""
	l = []
	try:
		with open(file, "r") as f:
			for line in f:
				parsedLine = line.strip('\t\n\r').split('\t')
				l.append(parsedLine)
	except FileNotFoundError:
		print("Place file in main directory or update filename in the script.")
		raise
	headerList = l[0]
	rawDataList = l[1:]
	return headerList, rawDataList


def make_default_json(inArgs, hasCoeff, coeffType):
	"""
	Create JSON that is constant for all genesets within the upload protocol
	
	:param inArgs: <class 'argparse.Namespace'>
	:param hasCoeff: Boolean
	:param coeffType: String
	:return: Dict
	"""
	default_json = dict()
	default_json['source'] = inArgs.so
	default_json['subtype'] = inArgs.st
	default_json['taxId'] = inArgs.ti
	default_json['user'] = inArgs.us
	default_json['domain'] = inArgs.do

	default_json['hasQC'] = False
	default_json['comment'] = ''
	default_json['date'] = datetime.datetime.utcnow()
	default_json['hasCoeff'] = hasCoeff
	if coeffType is not None:
		default_json['coeffType'] = coeffType

	return default_json
	
	
def make_api_default_json(params, hasCoeff, coeffType):
	"""
	Functional duplicate for 'make_default_json'
	
	:param params: Dict
	:param hasCoeff: Boolean
	:param coeffType: String
	:return: Dict
	"""
	default_json = dict()
	default_json['source'] = params['so']
	default_json['taxId'] = params['ti']
	default_json['user'] = params['us']
	
	if 'st' in params:
		default_json['subtype'] = params['st']
	else:
		default_json['subtype'] = ''
		
	if 'do' in params:
		default_json['domain'] = params['do']
	else:
		default_json['domain'] = ''

	default_json['hasQC'] = False
	default_json['comment'] = ''
	default_json['date'] = datetime.datetime.utcnow()
	default_json['hasCoeff'] = hasCoeff
	if coeffType is not None:
		default_json['coeffType'] = coeffType

	return default_json
	

def make_col_search_dict(headerList, geneFormat):
	"""
	Create a dictionary with future database field as key and the column reference as field
	
	:param headerList: List<String>
	:param geneFormat: Int
	:return searchDict: Dict - {'accepted': Dict<>, 'meta': Dict<>}
	:return useCoeff: Boolean
	:return coeffType: String
	"""
	# Check both 'setName' and 'genes' headers are in headerList
	geneCoeffHeaderFormat = 'genes | '
	assert 'setName' in headerList
	assert headerList[-1] == 'genes' or headerList[-1].startswith(geneCoeffHeaderFormat)
	
	# If gene has a coefficient, make constant variables => 'coeffType', 'useCoeff'
	if headerList[-1].startswith(geneCoeffHeaderFormat):
		coeffType = headerList[-1].split(geneCoeffHeaderFormat)[1]
		useCoeff = True
	else:
		coeffType = None
		useCoeff = False
	headerList[-1] = 'genes'
	
	# Scrape indexes from (updated) headerList
	rawDict = {headerList[i]: i for i in range(len(headerList))}
	
	# Identify meta-tags and separate
	acceptedTags = {k: v for k, v in rawDict.items() if k in ACCEPTED_HEADERS}
	acceptedTags['genes'] = {'startCol': acceptedTags['genes'], 'format': geneFormat, 'num': useCoeff}
	metaTags = {k: v for k, v in rawDict.items() if k not in ACCEPTED_HEADERS}
	
	searchDict = {'accepted': acceptedTags, 'meta': metaTags}
	return searchDict, useCoeff, coeffType
	

def genesQC(genesArray):
	"""
	If the gene array is full, return True. 
	
	:param genesArray: List of [[a, b, c, d], x]
	:return: Boolean
	"""
	return all(all(x != '' for x in gene[0]) for gene in genesArray)
	

def make_batch_input(genesetList, searchDict, constantJSON):
	"""	
	:param genesetList: List<String>
	:param searchDict: Dict
	:param constantJSON: Dict
	:return: List<Dict>
	"""
	outputList = []
	for parsedLine in genesetList:
		d = {}
		
		# Iterate over keys in searchDict['accepted']
		for k, v in searchDict['accepted'].items():
			if k == 'genes':
				rawGeneset = parsedLine[v['startCol']:]
				formatN = v['format']
				
				# Format 1: 'GENE'
				if v['num'] == False:
					orgGene = []
					for gene in rawGeneset:
						geneArray = getGeneArray(gene, constantJSON['taxId'], formatN)
						# geneArray = [''] * 4
						# geneArray[formatN] = gene
						orgGene.append([geneArray, None])
				
				# Format 2: 'GENE | VALUE'
				else:
					splitGeneset = [ent.split(' | ') for ent in rawGeneset]
					orgGene = []
					for entry in splitGeneset:
						geneArray = getGeneArray(entry[0], constantJSON['taxId'], formatN)
						# geneArray = [''] * 4
						# geneArray[formatN] = entry[0]
						orgGene.append([geneArray, float(entry[1])])
				
				d['genes'] = orgGene
			else:
				d[k] = parsedLine[v]
		
		# Iterate over keys in searchDict['meta']
		if len(searchDict['meta']) > 0:
			metaDict = dict()
			for k, v in searchDict['meta'].items():
				metaDict[k] = parsedLine[v]
			d['meta'] = metaDict
	
		outD = dict(list(d.items()) + list(constantJSON.items()))
		
		# Quality check gene format
		outD['hasQC'] = genesQC(outD['genes'])
		
		# Append geneset to batch list
		outputList.append(outD)
	return outputList