import xmltodict

FILE_LOC = './feed.xml'

SPLIT_BY_PARAMS = ['@CATEGORY_CODE', '@SUB_CATEGORY_CODE', '@ORGANISM']
ADD_REMOVE_TAGS = ['@MEMBERS', '@MEMBERS_SYMBOLIZED', '@MEMBERS_MAPPING']
SET_NAME_TAG = '@STANDARD_NAME'
GENES_TAG = '@MEMBERS_EZID'


def parseXml(file_loc):
    """
    Parse full MSigDB .xml file into a nested OrderedDict

    :param file_loc: String
    :return: OrderedDict
    """
    try:
        with open(file_loc, "rb") as f:
            d = xmltodict.parse(f, xml_attribs=True)
    except FileNotFoundError:
        print("Place file in main directory or update filename in the script.")
        raise

    try:
        return d['MSIGDB']['GENESET']
    except KeyError:
        print("XML tags have been modified - please adjust accordingly.")
        raise


def main():
	parsed = parseXml('./feed.xml')

	# Separate genesets into categories (Cat-Subcat-Organism)
	uniqueGMTXDict = dict()
	for geneset in parsed:
		keyList = [geneset[param] for param in SPLIT_BY_PARAMS]
		key = '_'.join(keyList)
		if key not in uniqueGMTXDict:
			uniqueGMTXDict[key] = [geneset]
		else:
			uniqueGMTXDict[key].append(geneset)

	removeKeys = SPLIT_BY_PARAMS + ADD_REMOVE_TAGS + [SET_NAME_TAG, GENES_TAG]
	extractKeys = [key for key in parsed[0].keys() if key not in removeKeys]
	header = ['setName'] + extractKeys + ['genes']

	for k, v in uniqueGMTXDict.items():
		# Generate write out list
		writeOut = []
		for gs in v:
			name = gs[SET_NAME_TAG]
			values = [gs[s] for s in extractKeys]
			genes = gs[GENES_TAG].split(',')
			gsOut = [name] + values + genes
			writeOut.append(gsOut)
		
		# Write out
		outFileName = k + '.gmtx'
		with open(outFileName, 'w', encoding='utf-8') as f:
			f.write('\t'.join(header) + '\n')
			for l in writeOut:
				f.write('\t'.join(l) + '\n')
				

if __name__ == "__main__":
	main()
