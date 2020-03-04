"""
====================================================================
creeds_to_gmtx.py: Converting CREEDS genesets into .gmtx file format
====================================================================
__contact__ = 'swk30.cam@gmail.com'
__date__ = '19.11.2018'
__status__ = 'MVP Complete'

"""

import json
import argparse
import os

ACCEPT_KEYS = ['up_genes', 'down_genes']
ACCEPT_TYPES = ["<class 'str'>", "<class 'int'>"]
GENESET_ID_KEY = 'id'
ORGANISM_KEY = 'organism'


def getGmtxHeaders(d):
	"""
	:param d: Dict
	:return: List<String>
	"""
	checkDict = {k: str(type(v)) for k, v in d.items()}
	allowList = []
	for k, v in checkDict.items():
		if k in ACCEPT_KEYS:
			allowList.append(k)
		elif v in ACCEPT_TYPES:
			allowList.append(k)
	return allowList


def valGenesetToString(l):
	"""
	:param l: List<List<String (Gene), Float (Coeff)>>
	:return: List<String>
	"""
	return [x[0] + ' | ' + str(x[1]) for x in l]
	

def main():
	# Command-line input
	parser = argparse.ArgumentParser()
	parser.add_argument('--f', type=str, help='File location')
	args = parser.parse_args()
	assert os.path.isfile(args.f)
	inFileLoc = args.f
	outFileLoc = '.'.join(inFileLoc.split('.')[:-1]) + '.gmtx'

	# Get the CREEDS <LIST> of GENESET SIGNATURES (UP AND DOWN)
	with open(inFileLoc, 'r') as f:
		rawLoad = json.load(f)
	assert isinstance(rawLoad, list)
	allHeaders = getGmtxHeaders(rawLoad[0])
	assert GENESET_ID_KEY in allHeaders
	assert any(x in allHeaders for x in ACCEPT_KEYS)
	
	# Get headers
	gmtxMetaHeaders = [x for x in allHeaders if x not in ACCEPT_KEYS + [GENESET_ID_KEY]]	
	gmtxHeaders = ['setName'] + gmtxMetaHeaders + ['genes | CD']
	rawWriteOut = []
	
	# Geneset extraction logic
	for d in rawLoad:
		genesetDict = {x: d[x] for x in allHeaders}
		if 'up_genes' in genesetDict:
			_upMeta = [str(genesetDict[k]).replace('\t', ' ').replace('\n', ' ') for k in gmtxMetaHeaders]
			_upId = [genesetDict['id'] + '_UP']
			_upGenes = valGenesetToString(genesetDict['up_genes'])
			_up = _upId + _upMeta + _upGenes
			rawWriteOut.append(_up)
		if 'down_genes' in genesetDict:
			_dnMeta = [str(genesetDict[k]).replace('\t', ' ').replace('\n', ' ') for k in gmtxMetaHeaders]
			_dnId = [genesetDict['id'] + '_DN']
			_dnGenes = valGenesetToString(genesetDict['down_genes'])
			_dn = _dnId + _dnMeta + _dnGenes
			rawWriteOut.append(_dn)
	
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
