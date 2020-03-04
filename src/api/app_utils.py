def similarity_jaccard(a, b):
	"""
	Given two genesets, returns a similarity measure based on the
	Jaccard coefficient:
	
	k(a, b) = (a AND b) / (a OR B)
	
	:param a: Set<String>
	:param b: Set<String>
	:return: Float
	"""
	intersect = len(set.intersection(a, b))
	union = len(set.union(a, b))
	k = float(intersect / union)
	return k

	
def similarity_overlap(a, b):
	"""
	Given two genesets, returns a similarity measure based on the
	Szymkiewicz–Simpson (overlap) coefficient:
	
	k(a, b) = (a AND b) / MIN(a, b)
	
	:param a: Set<String>
	:param b: Set<String>
	:return: Float
	"""
	intersect = len(set.intersection(a, b))
	minimum = min(len(a), len(b))
	try:
		k = float(intersect / minimum)
	except ZeroDivisionError:
		k = 0
	return k