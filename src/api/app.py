"""
===============================
app.py: RESTful API for GeMS
===============================
__contact__ = 'swk30.cam@gmail.com'
__date__ = '10.10.2018'
__status__ = 'MVP Complete'
"""

# Dependencies

import os
import sys

from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource

from app_utils import similarity_jaccard, similarity_overlap
from upload import api_insert
from db_config import COLLECTION_NAME
from db_utils import db, INDEX_LIST


# Code

app = Flask(__name__)
api = Api(app, catch_all_404s=True)


class Genesets(Resource):
	def __init__(self):
		self.returnParamNames = 'returnParams'
		self.genesParam = 'genes'


	def getOutput(self, query, returnParams, geneList):
		"""
		:param query: Dict
		:param returnParams: List<String> or None
		:param geneList: List<String> or None
		:return: List
		"""
		if geneList is not None:
			geneMatchList = [{'genes': {'$elemMatch': {'$elemMatch': {'$elemMatch': {'$in': [gene]}}}}} for gene in geneList]
			otherQueryList = [{k: v} for k, v in query.items()]
			geneQuery = {'$and': geneMatchList + otherQueryList}
			query = geneQuery
			
		if 'setName' in query:
			queryString = query['setName']
			queryJSON = {'$regex': queryString}
			query['setName'] = queryJSON
		
		output = []
		q = db[COLLECTION_NAME].find(query)
		for p in q:
			if returnParams == None:
				docReturn = {k: v for k, v in p.items() if k != '_id'}
			else:
				docReturn = dict()
				for param in returnParams:
					if param in p:
						docReturn[param] = p[param]
					else:
						docReturn[param] = ""
			output.append(docReturn)
		return output
	

	def get(self):
		parsedArgs = request.args
		data = {k: v for k, v in parsedArgs.items()}
		hasGenes = False
		params = data.pop(self.returnParamNames, None)
		genes = data.pop(self.genesParam, None)
		if params is not None:
			params = params.split(',')
		if genes is not None:
			genes = genes.split(',')
			hasGenes = True
		
		# Determine output format (JSON or GMT file)
		getGmt = data.pop('getGmt', None)
		if getGmt in ['True', 'true']:
			getGmt = True
		else:
			getGmt = False
		
		# Scrape data and present in established format
		if len(data) == 0 and hasGenes is False:
			# Error logic
			output = 404
			return jsonify({"response": output})
		elif getGmt:
			gmtParams = ['setName', 'desc', 'genes']
			output = self.getOutput(data, gmtParams, genes)
			
			# outputList: list of tab-delimited String (setName-desc-genes)
			outputList = []
			for gs in output:
				name = [gs['setName']]
				desc = [gs['desc']]
				genes = [gene[0][2] for gene in gs['genes'] if gene[0][2] != '']
				combined = name + desc + genes
				combinedStr = '\t'.join(combined)
				outputList.append(combinedStr)
			
			# Output: GMT file
			tsv = '\n'.join(outputList)
			response = make_response(tsv)
			response.headers['content-type'] = 'application/octet-stream'	
			return response
		else:
			# Output: JSON
			output = self.getOutput(data, params, genes)
			return jsonify({"response": output})


	def post(self):
		data = request.get_json()
		hasGenes = False
		params = data.pop(self.returnParamNames, None)
		genes = data.pop(self.genesParam, None)
		if genes is not None:
			hasGenes = True
		
		if len(data) == 0 and hasGenes is False:
			output = 404
		else:
			output = self.getOutput(data, params, genes)
		return jsonify({"response": output})


class Similar(Resource):
	def __init__(self):
		self.requiredParams = {'setName', 'source', 'subtype', 'user', 'method', 'threshold'}
		self.acceptedMethods = {'jaccard', 'overlap'}
		self.getGeneSet = lambda l : {gene[0][2] for gene in l if gene[0][2] != ''}


	def getGeneMembers(self, inputDict):
		"""
		:param inputDict: Dict
		:return: Set - Empty if invalid
		"""
		testParams = {x for x in inputDict.keys()}
		findGeneset = db[COLLECTION_NAME].find_one({
			'setName': inputDict['setName'],
			'source': inputDict['source'],
			'subtype': inputDict['subtype'],
			'user': inputDict['user']
		})
		if testParams != self.requiredParams:
			return set()
		elif not inputDict['threshold'].replace('.', '').isdigit():
			return set()
		elif inputDict['method'] not in self.acceptedMethods:
			return set()
		elif findGeneset is None:
			return set()
		else:
			returnGenes = self.getGeneSet(findGeneset['genes'])
			return returnGenes


	def get(self):
		parsedArgs = request.args
		input = {k: v for k, v in parsedArgs.items()}
		
		genes = self.getGeneMembers(input)
		if len(genes) == 0:
			output = 404
		else:
			output = []
			method = input['method']
			threshold = float(input['threshold'])
			
			# Optimisation: ignore geneset with which the intersection will just be 0
			allGenesets = db[COLLECTION_NAME].find({'genes': {'$elemMatch': {'$elemMatch': {'$elemMatch': {'$in': list(genes)}}}}})
			for geneset in allGenesets:
				compareGenes = self.getGeneSet(geneset['genes'])
				if method == 'jaccard':
					sim = similarity_jaccard(compareGenes, genes)
				elif method == 'overlap':
					sim = similarity_overlap(compareGenes, genes)
				
				if sim >= threshold:
					output.append({'setName': geneset['setName'],
									'source': geneset['source'],
									'coeff': sim
					})
				
		return jsonify({"response": output})

		
class addGenesets(Resource):
	def post(self):
		data = request.get_json()
		
		if set(data.keys()) != {'headers', 'parsed', 'params'}:
			output = 404
		else:
			try:
				output = [200] + api_insert(data['headers'], data['parsed'], data['params'])
			except AssertionError:
				output = 404
			except Exception:
				output = 404

		return jsonify({"response": output})
		
		
class delGenesets(Resource):
	def post(self):
		data = request.get_json()
		
		try:
			assert 'genesets' in data
			removeList = data['genesets']
			for geneset in removeList:
				assert set(geneset.keys()) == set(INDEX_LIST)
				assert geneset['user'] != 'Public'
				db[COLLECTION_NAME].remove(geneset)
			output = 200
		except AssertionError:
			output = 404
		except Exception:
			output = 404

		return jsonify({"response": output})


api.add_resource(Genesets, "/api/genesets")
api.add_resource(Similar, "/api/similar")
api.add_resource(addGenesets, "/api/insert")
api.add_resource(delGenesets, "/api/remove")


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1234, debug=True)
