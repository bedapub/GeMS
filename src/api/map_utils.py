'''
============================================
map_utils.py: Utils relating to gene mapping
============================================
__author__ = "Albert Kang"
__email__ = "swk30.cam@gmail.com"
__date__ = "06.12.2018"
__status__ = "In progress"


Test - [Tubb2a, 498736, TUBB2A, 7280] : taxId = 10116

Positive tests:
	> getFromNativeId(nId=498736, taxId=10116)            => ['Tubb2a', '498736', 'TUBB2A', '7280']
	> getFromNativeSymbol(nSym='Tubb2a', taxId=10116)     => ['Tubb2a', '498736', 'TUBB2A', '7280']
	> getFromHumanisedId(hId=7280, taxId=10116)           => ['Tubb2a', '498736', 'TUBB2A', '7280']
	> getFromHumanisedSymbol(hSym='TUBB2A', taxId=10116)  => ['Tubb2a', '498736', 'TUBB2A', '7280']
Negative tests:
	> getFromNativeSymbol(nSym='X', taxId=10116)       => ['X', '', '', '']

'''

import os
import sys

from db_config import GENE_COL, MAPPING_COL
from db_utils import db

HUMAN_TAX_ID = 9606


def _mapIdtoId(id, mapTo):
	"""
	Get the homolog gene ID from taxId A to taxId B.
	Look up from Homologene collection.
	
	:param id: Int - Gene ID
	:param mapTo: Int - Taxonomy ID
	:return: List<Int> - Gene ID (generally should only contain 1 gene ID)
	"""
	id = int(id)
	_match = {'$match': {"members.taxId": mapTo, "members.geneId": id}}
	_project = {'$project': {
			'members': {
				'$filter': {
					'input': '$members',
					'as': 'member',
					'cond': { '$eq': [ '$$member.taxId', mapTo ] }
				}
			}
		}
	}
	filterLogic = [_match, _project]
	mapQuery = db[MAPPING_COL].aggregate(filterLogic)
	mappedIds = [x['geneId'] for l in mapQuery for x in l['members']]
	return mappedIds


def _idToSym(id):
	"""
	Get the gene symbol given the Gene ID.
	Look up from the NCBI gene information collection.
	
	:param id: Int - Gene ID
	:return: String - Gene symbol
	"""
	id = int(id)
	findDict = db[GENE_COL].find_one({'geneId': id})
	if findDict == None:
		print("Error: Gene ID - " + str(id) + " is not valid.")
		geneSymbol = ""
	else:
		geneSymbol = findDict['Symbol']
	return geneSymbol
	
	
def _symToId(sym, taxId):
	"""
	Get the gene ID given the gene symbol and taxonomy ID.
	Look up from the NCBI gene information collection.
	
	:param sym: String
	:param taxId: Int or String<Empty>
	"""
	findDict = db[GENE_COL].find_one({'Symbol_official': sym, 'taxId': taxId})
	if findDict == None:
		findDict = db[GENE_COL].find_one({'Symbol': sym, 'taxId': taxId})
	if findDict == None:
		# Try synonym search before error
		findSynonyms = db[GENE_COL].find({'Synonyms': sym, 'taxId': taxId})
		if findSynonyms.count() == 1:
			geneId = findSynonyms[0]['geneId']
		else:
			print("Error: " + sym + " (taxId  " + str(taxId) + ") is not valid.")
			geneId = ""
	else:
		geneId = findDict['geneId']
	return geneId


def getFromNativeId(nId, taxId):
	"""
	Infer the 4-element gene array from the native (original)
	gene ID

	:param nId: Int
	:param taxId: Int
	:return: List<String>
	"""
	nSym = _idToSym(nId)
	if taxId == HUMAN_TAX_ID:
		hId = nId
		hSym = nSym
	else:
		rawMapId = _mapIdtoId(nId, HUMAN_TAX_ID)
		if len(rawMapId) != 1:
			hId = ""
			hSym = ""
		else:
			hId = rawMapId[0]
			hSym = _idToSym(hId)
	
	returnArray = [nSym, nId, hSym, hId]
	returnArray = [str(x) for x in returnArray]
	return returnArray
	

def getFromHumanisedId(hId, taxId):
	"""
	Infer the 4-element gene array from the humanised
	gene ID

	:param hId: Int
	:param taxId: Int
	:return: List<String>
	"""
	hSym = _idToSym(hId)
	if taxId == HUMAN_TAX_ID:
		nId = hId
		nSym = hSym
	else:
		rawMapId = _mapIdtoId(hId, taxId)
		if len(rawMapId) != 1:
			nId = ""
			nSym = ""
		else:
			nId = rawMapId[0]
			nSym = _idToSym(nId)
	
	returnArray = [nSym, nId, hSym, hId]
	returnArray = [str(x) for x in returnArray]
	return returnArray


def getFromNativeSymbol(nSym, taxId):
	"""
	Infer the 4-element gene array from the native (original)
	gene symbol

	:param nSym: String
	:param taxId: Int
	:return: List<String>
	"""
	nId = _symToId(nSym, taxId)
	if taxId == HUMAN_TAX_ID:
		hId = nId
		hSym = nSym
	elif nId == "":
		hId = ""
		hSym = ""
	else:
		rawMapId = _mapIdtoId(nId, HUMAN_TAX_ID)
		if len(rawMapId) != 1:
			hId = ""
			hSym = ""
		else:
			hId = rawMapId[0]
			hSym = _idToSym(hId)
			
	returnArray = [nSym, nId, hSym, hId]
	returnArray = [str(x) for x in returnArray]
	return returnArray


def getFromHumanisedSymbol(hSym, taxId):
	"""
	Infer the 4-element gene array from the humanised
	gene symbol

	:param hSym: String
	:param taxId: Int
	:return: List<String>
	"""
	hId = _symToId(hSym, HUMAN_TAX_ID)
	if taxId == HUMAN_TAX_ID:
		nId = hId
		nSym = hSym
	elif hId == "":
		nId = ""
		nSym = ""
	else:
		rawMapId = _mapIdtoId(hId, taxId)
		if len(rawMapId) != 1:
			nId = ""
			nSym = ""
		else:
			nId = rawMapId[0]
			nSym = _idToSym(nId)
			
	returnArray = [nSym, nId, hSym, hId]
	returnArray = [str(x) for x in returnArray]
	return returnArray


def getGeneArray(inputGene, taxId, geneFormat):
	"""
	Main control unit for gene array mapping and inference.
	
	0 -> Native gene symbol
	1 -> Native gene ID
	2 -> Humanised gene symbol
	3 -> Humanised gene ID
	
	:param inputGene: Int or String
	:param taxId: Int
	:param geneFormat: Int
	:return: List<String>
	"""
	if geneFormat == 0:
		return getFromNativeSymbol(inputGene, taxId)
	elif geneFormat == 1:
		return getFromNativeId(inputGene, taxId)
	elif geneFormat == 2:
		return getFromHumanisedSymbol(inputGene, taxId)
	elif geneFormat == 3:
		return getFromHumanisedId(inputGene, taxId)

