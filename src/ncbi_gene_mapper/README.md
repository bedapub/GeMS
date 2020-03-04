1. Retrieve raw files from the NCBI repository
```
[\GeMS\tools\gene_mapping] wget ftp://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz -O gene_info.gz
[\GeMS\tools\gene_mapping] wget ftp://ftp.ncbi.nih.gov/pub/HomoloGene/current/homologene.data -O homologene.data
```

2. Unzip the files
```
[\GeMS\tools\gene_mapping] gunzip < gene_info.gz > gene_info.txt
```

3. Scrape and upload
```
[\GeMS\tools\gene_mapping] python run.py
```

N.B. Add two indexes on the 'GeMS_gene_info' collection for faster queries:
- {'geneId': 1}
- {'taxId': 1, 'Symbol': 1} 
