import json
import sys
from WikiSearch.QueryParser import QueryParser

def search_by_keywords(keywords):
	qp = QueryParser()
	doc_id_list = qp.query(keywords)
	result = []
	for doc_id in doc_id_list:
		file_path = "DocumentContent/" + str(doc_id)
		with open(file_path, 'r') as f:
			result.append([doc_id, f.read()])
	return result