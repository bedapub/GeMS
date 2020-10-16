# Programmatic Access to GeMS via RESTful API

The Flask-RESTful API is deployed on base URL, *http://biocomp:1234/api/*, over four endpoints:
  
| Endpoints     | API Protocols  |
|:-------------:|:--------------:|
| `/genesets`   | POST, GET      |
| `/similar`    | POST, GET      |  
| `/insert`     | POST           |    
| `/remove`     | POST           |       

## Contents
<!--ts-->
   * [1. Querying the genesets collection - */genesets*](#1-querying-the-genesets-collection-----genesets-)
   * [2. Geneset similarity analysis - */similar*](#2-geneset-similarity-analysis-----similar-)
   * [3. Adding and removing genesets - */insert* and */remove*](#3-adding-and-removing-genesets-----insert--and---remove-)
<!--te-->

## 1. Querying the genesets collection - */genesets*

The parameter names for the queries are identical to the field names in the MongoDB genesets collection.
Please refer the main README to find out more about the fields.

To note:
  - The `genes` parameter accepts multiple genes in a comma-delimited format - see the example below.
  - The `returnParams` parameter takes a comma-delimited String which can be used to specify the fields that you would like returned.
  - The GET request has an additional parameter, `getGmt`, which takes a boolean value to return a GMT file of your API query.
  
The parameters are as follows:

| Fields         | Stable    | Type      | API Protocol  |
|:--------------:|:---------:|:---------:|:-------------:|                 
| `setName`      |   O       |  String   |  GET, POST    |          
| `source`       |   O       |  String   |  GET, POST    |           
| `subtype`      |   O       |  String   |  GET, POST    |         
| `user`         |   O       |  String   |  GET, POST    |         
| `domain`       |   O       |  String   |  GET, POST    |         
| `comment`      |   O       |  String   |  GET, POST    |         
| `genes`        |   O       |  String*  |  GET, POST    |         
| `taxId`        |   O       |  Int      |  POST         |  
| `hasCoeff`     |   O       |  Boolean  |  POST         |  
| `hasQC`        |   O       |  Boolean  |  POST         |  
| `date`         |   O       |  Date     |  POST         |  
| `xref`         |   X       |  String   |  GET, POST    |        
| `setId`        |   X       |  String   |  GET, POST    |        
| `desc`         |   X       |  String   |  GET, POST    |        
| `coeffType`    |   X       |  String   |  GET, POST    |        
| `meta`         |   X       |  Object   |  GET^, POST   |         
| `returnParams` |  N/A      |  String*  |  GET, POST    |        
| `getGmt`       |  N/A      |  Boolean  |  GET          |

`*`: comma-separated          
`^`: `if type(meta.X) == String`

### Example 1 - Get the set names of the genesets that have the subtype 'disease'

GET URL: *http://biocomp:1234/api/genesets?subtype=disease&returnParams=setName*

In Python:
```
from requests import post, get

BASE_URL = 'http://biocomp:1234/api/genesets'

# POST

dataIn = {
    'subtype': 'disease',
    'returnParams': ['setName']
}
			
returnJSON = post(BASE_URL, json=dataIn).json()

# GET

get_req = '?subtype=disease&returnParams=setName'
request = BASE_URL + get_req

returnJSON = get(request).json()
```

In R:
```
library(httr)
library(jsonlite)

BASE_URL <- 'http://biocomp:1234/api/genesets'

# POST

dataIn <- list(
    subtype = "disease",
    returnParams = c("setName")
)

response <- POST(HOST_URL, body=dataIn, encode='json')
returnJSON <- fromJSON(httr::content(response, 'text'))

# GET

get_req <- "?subtype=disease&returnParams=setName"
request <- paste(BASE_URL, get_req, sep="")

response <- GET(request)
returnJSON <- fromJSON(httr::content(response, 'text'))
```

### Example 2a: Get the set names of the genesets with genes: GNB1, GNB2 and GMB3

GET URL: *http://biocomp:1234/api/genesets?genes=GNB1,GNB2,GNB3&returnParams=setName*

In Python:
```
# POST

dataIn = {
    'genes': ['GNB1', 'GNB2', 'GNB3'],
    'returnParams': ['setName']
}
		
returnJSON = post(BASE_URL, json=dataIn).json()

# GET

get_req = '?genes=GNB1,GNB2,GNB3&returnParams=setName'
request = BASE_URL + get_req

returnJSON = get(request).json()
```

In R:
```
# POST

dataIn <- list(
    genes = c("GNB1", "GNB2", "GNB3"),
    returnParams = c("setName")
)

response <- POST(HOST_URL, body=dataIn, encode='json')
returnJSON <- fromJSON(httr::content(response, 'text'))

# GET

get_req <- "?genes=GNB1,GNB2,GNB3&returnParams=setName"
request <- paste(BASE_URL, get_req, sep="")

response <- GET(request)
returnJSON <- fromJSON(httr::content(response, 'text'))
```

### Example 2b: Get the GMT file of the genesets with genes: GNB1, GNB2 and GMB3 (Shell script)
```
wget http:/biocomp:1234/api/genesets?genes=GNB1,GNB2,GNB3&returnParams=setName&getGmt=True
```

## 2. Geneset similarity analysis - */similar*

As we have a centralised repository of structured geneset documents from multiple sources,
we can now examine the uniqueness of our geneset (or, how similar a geneset is to a different
geneset in the GeMS database).

There are 6 mandatory parameters:
  - `setName` - String
  - `source` - String
  - `user` - String
  - `subtype` - String
  - `method` - String
  - `threshold` - Float (between 0 and 1)
	
`setName`, `source`, `user` and `subtype` are the fields in our collections that define a unique geneset.

`method` defines the similarity coefficient that we are using. Currently, we only support 'jaccard' and 'overlap'. 
The parameter `threshold` filters genesets with coeffient less than the given value.

### Example: Get genesets that are similar with geneset (dz:770_UP, CREEDS, Public, disease) to a degree greater than 0.5 using the overlap similarity coefficient

GET URL: *http://biocomp:1234/api/similar?setName=dz:770_UP&source=CREEDS&user=Public&subtype=disease&method=overlap&threshold=0.5*

In Python:
```
BASE_URL = 'http://biocomp:1234/api/similar'

# POST

dataIn = {
    'setName': 'dz:770_UP',
    'source': 'CREEDS',
    'user': 'Public'
    'subtype': 'disease',
    'method': 'overlap',
    'threshold': '0.5'
}
			
returnJSON = post(BASE_URL, json=dataIn).json()

# GET

get_req = '?setName=dz:770_UP&source=CREEDS&user=Public&subtype=disease&method=overlap&threshold=0.5'
request = BASE_URL + get_req

returnJSON = get(request).json()
```

In R:
```
BASE_URL <- 'http://biocomp:1234/api/similar'

# POST

dataIn <- list(
    setName = "dz:770_UP",
    source = "CREEDS",
    user = "Public",
    subtype = "disease",
    method = "overlap",
    threshold = "0.5"
)

response <- POST(HOST_URL, body=dataIn, encode='json')
returnJSON <- fromJSON(httr::content(response, 'text'))

# GET

get_req <- "?setName=dz:770_UP&source=CREEDS&user=Public&subtype=disease&method=overlap&threshold=0.5"
request <- paste(BASE_URL, get_req, sep="")

response <- GET(request)
returnJSON <- fromJSON(httr::content(response, 'text'))
```

## 3. Adding and removing genesets - */insert* and */remove*

See Jupyter notebooks for examples...
  - in Python: *https://github.com/bedapub/GeMS/blob/master/examples/Python_Add_Remove_Genesets.ipynb*
  - in R: *https://github.com/bedapub/GeMS/blob/master/examples/R_Add_Remove_Genesets.ipynb*
