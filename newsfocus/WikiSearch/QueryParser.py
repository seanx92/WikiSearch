import subprocess
import os
from nltk.stem.snowball import SnowballStemmer

def doc_list_compare_in_id(a, b):
	return a[0] < b[0]

class DocList:
	__is_not_flag = []
	__doc_list = []

	def __init__(self, doc_list, is_not_flag):
		self.__doc_list = doc_list
		self.__is_not_flag = is_not_flag
		self.__doc_list.sort(doc_list_compare_in_id)

	def get_ranked(self):
		return [entry[0] for entry in sorted(self.__doc_list, key=lambda x: x[1], reverse=True)[0:100]]

	def intersect(self, second):
		if self.__is_not_flag:
			list_a = second.get_list()
			list_b = self.get_list()
		elif second.is_not:
			list_a = self.get_list()
			list_b = second.get_list()
		ret = []
		pa = pb = 0

		if self.__is_not_flag or second.is_not():
			while pa < len(list_a) and pb < len(list_b):
				if list_a[pa][0] < list_b[pb][0]:
					ret.append(list_a[pa])
					pa += 1
				elif list_a[pa][0] > list_b[pb][0]:
					pb += 1
				else:
					pa += 1
					pb += 1
			while pa < len(list_a):
				ret.append(list_a[pa])
				pa += 1
		else:
			while pa < len(list_a) and pb < len(list_b):
				if list_a[pa][0] > list_b[pb][0]:
					pb += 1
				elif list_a[pa][0] < list_b[pb][0]:
					pa += 1
				else:
					ret.append([list_a[pa][0], list_a[pa][1] * list_b[pb][1]])
					pa += 1
					pb += 1
		return DocList(ret, False)

	def union(self, second):
		list_a = self.get_list()
		list_b = second.get_list()
		ret = []
		pa = pb = 0
		while pa < len(list_a) and pb < len(list_b):
			if list_a[pa][0] < list_b[pb][0]:
				ret.append(list_a[pa])
				pa += 1
			elif list_a[pa][0] > list_b[pb][0]:
				ret.append(list_b[pb])
				pb += 1
			else:
				ret.append([list_a[pa][0], list_a[pa][1] + list_b[pb][1]])
				pa += 1
				pb += 1
		while pa < len(list_a):
			ret.append(list_a[pa])
			pa += 1
		while pb < len(list_b):
			ret.append(list_b[pb])
			pb += 1

		return DocList(ret, False)

	def get_list(self):
		return self.__doc_list

	def is_not(self):
		return self.__is_not_flag

class QueryParser:

	term_set = {}
	stemmer = SnowballStemmer("english")

	def stem(self, term):
		term = self.debracket(term).strip()
		return self.stemmer.stem(term)

	def query(self, query):
		query = self.debracket(query)
		#self.get_tfidf(query)
		self.setup()
		doc_list = self.query_and(query)
		ranked_doc_list = doc_list.get_ranked()
		#self.get_document_content(ranked_doc_list)
		return ranked_doc_list

	def get_document_content(self, doc_list):
		command = ['newsfocus/WikiSearch/GetDocuments.sh']
		command += [str(doc_id) for doc_id in doc_list]
		print command
		subprocess.check_output(command)

	def get_tfidf(self, query):
		query = query.replace("AND", "")
		query = query.replace("OR", "")
		query = query.replace("NOT", "")
		query = query.replace("(", "")
		query = query.replace(")", "")
		terms = [self.stem(term) for term in query.split(" ") if len(term) > 0]
		cwd = os.getcwd()
		print "!!!!!!!!", cwd
		command = ['newsfocus/WikiSearch/Query.sh']
		command += terms
		print command
		subprocess.check_output(command)

	def setup(self):
		with open("TermsDocumentList") as f:
			for line in f:
				arr = line.split("\t")
				li = []
				for i in range(1, len(arr)):
					subarr = arr[i].split(" ")
					li.append([int(subarr[0]), float(subarr[1])])
				self.term_set[arr[0]] = li
		print self.term_set.keys()

	def query_and(self, query):
		query = self.debracket(query)
		subqueries = query.split("AND")
		curr = None
		for subquery in subqueries:
			doc_list = self.query_or(subquery)
			if curr is not None:
				curr = curr.intersect(doc_list)
			else:
				curr = doc_list
		return curr

	def query_or(self, query):
		query = self.debracket(query)
		subqueries = query.split("OR")
		curr = None
		for subquery in subqueries:
			doc_list = self.query_not(subquery)
			if curr is not None:
				curr = curr.union(doc_list)
			else:
				curr = doc_list
		return curr

	def get_list(self, term):
		if term in self.term_set:
			return self.term_set[term]
		else:
			print term
			raise Exception("Term not found!")

	def query_not(self, query):
		query = self.debracket(query).strip()

		if query.startswith("NOT "):
			term = self.stem(query[4:])
			return DocList(self.get_list(term), True)
		else:
			term = self.stem(query)
			return DocList(self.get_list(term), False)

	def debracket(self, query):
		query = query.strip()
		if len(query) > 0 and query[0] == '(' and query[len(query) - 1] == ')':
			return self.debracket(query[1:len(query) - 1])
		return query
