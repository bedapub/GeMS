#!/bin/bash

cd ./src/api


# Upload Reactome GMTx file (Gene format: 0)
printf "Uploading Reactome...\n"
python upload.py --fl ../../data/Reactome/ReactomePathways.gmtx --gf 0 --so Reactome --ti 9606 --us Public --do pathway


# Upload CellMarker GMTx files (Gene format: 1)
printf "\nUploading CellMarker...\n"
python upload.py --fl ../../data/CellMarker/Human_all_cell_markers.gmtx --gf 1 --so CellMarker --ti 9606 --us Public --do 'cell marker'
python upload.py --fl ../../data/CellMarker/Mouse_all_cell_markers.gmtx --gf 1 --so CellMarker --ti 10090 --us Public --do 'cell marker'


# Upload CREEDS GMTx files (Gene format: 0)
printf "\nUploading CREEDS...\n"
python upload.py --fl ../../data/CREEDS/human_disease_signatures-v1.0.gmtx --gf 0 --so CREEDS --ti 9606 --us Public --st disease
python upload.py --fl ../../data/CREEDS/human_single_drug_perturbations-v1.0.gmtx --gf 0 --so CREEDS --ti 9606 --us Public --st drug
python upload.py --fl ../../data/CREEDS/human_single_gene_perturbations-v1.0.gmtx --gf 0 --so CREEDS --ti 9606 --us Public --st gene
python upload.py --fl ../../data/CREEDS/mouse_disease_signatures-v1.0.gmtx --gf 0 --so CREEDS --ti 10090 --us Public --st disease
python upload.py --fl ../../data/CREEDS/mouse_single_drug_perturbations-v1.0.gmtx --gf 0 --so CREEDS --ti 10090 --us Public --st drug
python upload.py --fl ../../data/CREEDS/mouse_single_gene_perturbations-v1.0.gmtx --gf 0 --so CREEDS --ti 10090 --us Public --st gene
python upload.py --fl ../../data/CREEDS/rat_disease_signatures-v1.0.gmtx --gf 0 --so CREEDS --ti 10116  --us Public --st disease
python upload.py --fl ../../data/CREEDS/rat_single_drug_perturbations-v1.0.gmtx --gf 0 --so CREEDS --ti 10116  --us Public --st drug
python upload.py --fl ../../data/CREEDS/rat_single_gene_perturbations-v1.0.gmtx --gf 0 --so CREEDS --ti 10116  --us Public --st gene


# Upload MSigDB GMTx files (Gene format: 3)
printf "\nUploading MSigDB...\n"
python upload.py --fl ../../data/MSigDB/C1__Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C1
python upload.py --fl ../../data/MSigDB/C2_CGP_Danio\ rerio.gmtx --gf 3 --so MSigDB --us Public --ti 7955 --st C2 --do 'chemical and genetic peturbations'
python upload.py --fl ../../data/MSigDB/C2_CGP_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C2 --do 'chemical and genetic peturbations'
python upload.py --fl ../../data/MSigDB/C2_CGP_Macaca\ mulatta.gmtx --gf 3 --so MSigDB --us Public --ti 9544 --st C2 --do 'chemical and genetic peturbations'
python upload.py --fl ../../data/MSigDB/C2_CGP_Mus\ musculus.gmtx --gf 3 --so MSigDB --us Public --ti 10090 --st C2 --do 'chemical and genetic peturbations'
python upload.py --fl ../../data/MSigDB/C2_CGP_Rattus\ norvegicus.gmtx --gf 3 --so MSigDB --us Public --ti 10116 --st C2 --do 'chemical and genetic peturbations'
python upload.py --fl ../../data/MSigDB/C2_CP_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C2 --do 'canonical pathways'
python upload.py --fl ../../data/MSigDB/C3_MIR_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C3 --do 'microRNA targets'
python upload.py --fl ../../data/MSigDB/C3_TFT_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C3 --do 'transcription factor targets'
python upload.py --fl ../../data/MSigDB/C4_CGN_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C4 --do 'cancer gene neighbourhoods'
python upload.py --fl ../../data/MSigDB/C4_CM_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C4 --do 'cancer modules'
python upload.py --fl ../../data/MSigDB/C5_BP_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C5 --do 'biological process'
python upload.py --fl ../../data/MSigDB/C5_CC_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C5 --do 'cellular component'
python upload.py --fl ../../data/MSigDB/C5_MF_Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C5 --do 'molecular function'
python upload.py --fl ../../data/MSigDB/C6__Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C6
python upload.py --fl ../../data/MSigDB/C6__Mus\ musculus.gmtx --gf 3 --so MSigDB --us Public --ti 10090 --st C6
python upload.py --fl ../../data/MSigDB/C6__Rattus\ norvegicus.gmtx --gf 3 --so MSigDB --us Public --ti 10116 --st C6
python upload.py --fl ../../data/MSigDB/C7__Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st C7
python upload.py --fl ../../data/MSigDB/C7__Mus\ musculus.gmtx --gf 3 --so MSigDB --us Public --ti 10090 --st C7
python upload.py --fl ../../data/MSigDB/H__Homo\ sapiens.gmtx --gf 3 --so MSigDB --us Public --ti 9606 --st H
