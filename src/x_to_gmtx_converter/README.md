# Convert to GMTx format

## *file.x* -> *file.gmtx* 

Example given for: CellMarker, CREEDS, MSigDB

1. Download the raw files
```
mkdir CellMarker

wget http://biocc.hrbmu.edu.cn/CellMarker/download/all_cell_markers.txt -O CellMarker/all_cell_markers.txt

mkdir CREEDS

wget http://amp.pharm.mssm.edu/CREEDS/download/single_gene_perturbations-v1.0.json -O CREEDS/single_gene_perturbations-v1.0.json
wget http://amp.pharm.mssm.edu/CREEDS/download/single_drug_perturbations-v1.0.json -O CREEDS/single_drug_perturbations-v1.0.json
wget http://amp.pharm.mssm.edu/CREEDS/download/disease_signatures-v1.0.json -O CREEDS/disease_signatures-v1.0.json

mkdir MSigDB
[Manually download 'All gene sets - Current MSigDB xml file']
```

2. Convert

- Run 'CREEDS-to-GMTx' converter (suitable for CREEDS v1.0 - checked 03/Dec/2018)
```
python creeds_to_gmtx.py --f single_gene_perturbations-v1.0.json
	-> human_single_gene_perturbations-v1.0.gmtx
	-> mouse_single_gene_perturbations-v1.0.gmtx
	-> rat_single_gene_perturbations-v1.0.gmtx
	
python creeds_to_gmtx.py --f single_drug_perturbations-v1.0.json
	-> human_single_drug_perturbations-v1.0.gmtx
	-> mouse_single_drug_perturbations-v1.0.gmtx
	-> rat_single_drug_perturbations-v1.0.gmtx
	
python creeds_to_gmtx.py --f disease_signatures-v1.0.json
	-> human_disease_signatures-v1.0.gmtx
	-> mouse_disease_signatures-v1.0.gmtx
	-> rat_disease_signatures-v1.0.gmtx
```

- Run 'CellMarker-to-GMTx' converter (checked 03/Dec/2018)
```
python cellmarker_to_gmtx.py --f all_cell_markers.txt
	-> Human_all_cell_markers.gmtx
	-> Mouse_all_cell_markers.gmtx
```

- Run 'MSigDB-to-GMTx' converter (checked 11/Dec/2018)
```
python msigdb_to_gmtx.py
```

## *file.gmt* -> *file.gmtx* 

Example given for: Reactome

1. Download the raw file
```
mkdir Reactome
wget https://reactome.org/download/current/ReactomePathways.gmt.zip -O Reactome/ReactomePathways.gmt.zip
unzip ./Reactome/ReactomePathways.gmt.zip -d ./Reactome/
```

2. Add a header to the GMT file (note that the Reactome .GMT file is not really in an appropriate GMT format)
```
sed '1s/^/setName\tsetId\ttype\tgenes\n/' ReactomePathways.gmt > ReactomePathways.gmtx
```
