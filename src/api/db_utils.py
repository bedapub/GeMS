'''
====================================================
db_utils.py: Utils relating to database construction
====================================================
__author__ = "Albert Kang"
__email__ = "swk30.cam@gmail.com"
__date__ = "29.10.2018"
__status__ = "In progress"

Test MV-input:

{
    'setName': 'kjdhkjhd',
    'source': 'kjhkjh',
    'subtype': '',
    'taxId': 324,
    'hasCoeff': true,
    'genes': [[['a', 'b', 'c', 'd'], 2]],
    'user': 'kjhkjh',
    'domain': '',
    'hasQC': true,
    'comment': '',
    'date': ISODate("2018-08-31T14:48:03.321Z"),
}


'''
import os
import db_config as cf
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://{}:{}@{}:{}/{}'.format(
    cf.MONGODB_USERNAME,
    cf.MONGODB_PASSWORD,
    cf.MONGODB_HOST,
    cf.MONGODB_PORT,
    cf.MONGODB_DB
))


db = client[cf.MONGODB_DB]

INDEX_LIST = ['setName', 'source', 'subtype', 'user']

ACCEPTED_HEADERS = ['setName', 'genes', 'xref', 'setId', 'desc']
ACCEPTED_COEFF_TYPE = ['CD', 'logFC', 'SAM', 'limma', 'gini', 'DESeq']

FIELD_CONSTRAINTS = {'$jsonSchema': {
		'bsonType': "object",
		'required': ['setName',
					'source',
					'subtype',
					'taxId',
					'hasCoeff',
					'genes',
					'user',
					'domain',
					'hasQC', 
					'comment',
					'date'
					],
		'properties': {
			# Required
			'setName': {'bsonType': 'string'},
			'source': {'bsonType': 'string'},
			'subtype': {'bsonType': 'string'},
			'taxId': {'bsonType': 'int'},
			'hasCoeff': {'bsonType': 'bool'},
			'genes': {'bsonType': 'array'},
			'user': {'bsonType': 'string'},
			'domain': {'bsonType': 'string'},
			'hasQC': {'bsonType': 'bool'},
			'comment': {'bsonType': 'string'},
			'date': {'bsonType': 'date'},
			
			# Not required
			'xref': {'bsonType': 'string'},
			'setId': {'bsonType': 'string'},
			'desc': {'bsonType': 'string'},
			'meta': {'bsonType': 'object'},
			'coeffType': {'bsonType': 'string'}
		}
	}
}



def create_collection(db, name, constraints, indexAttrs):
	"""
	Create a collection with named 'name' with attribute constraints as in 'constraints'
	and a uniqueness constraint on 'unique'
	
	:param db: <class 'pymongo.database.Database'>
	:param name: String
	:param constraints: Dict
	:param uniqueField: String
	:return: VOID
	"""
	db.create_collection(
		name,
		validator=constraints
	)
	indexDict = [ (attr, pymongo.ASCENDING) for attr in indexAttrs ]
	db[name].create_index(indexDict, 
						unique=True, 
						background=True,
						name='geneset_uniqueness')
	

