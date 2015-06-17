#!/usr/bin/env python3

import nltk
import os
from segtok.segmenter import split_single as ssplit
try:
	from modules import sent_tokenize as st
except:
	import sent_tokenize as st

"""
papers.py
	A set of functions to deal with paper files created by pubcrawl/pubdip

"""

"""constants"""


stemmer = nltk.stem.snowball.EnglishStemmer()


"""
getNames:
	Given a file of abstracts, acquires the two terms to be searched from the file name

	file name is as follows:
		OBJECT_A#OBJECT_B
"""
def getNames(file):	
	def shorten(tup):
		return tup[0][0] + '. ' + tup[1]
	file = os.path.basename(file)
	name = os.path.splitext(file)[0]
	
	# print(name)
	name = [i.split('_') for i in name.split('#')]
	name = [[i.lower() for i in j] for j in name]
	#check if genus only
	# print(name)
	if len(name[0]) ==1:
			return [[i[0]] for i in name]

	return [[" ".join(i), shorten(i), i[0]] for i in name] 

		#([" ".join(name[0]), shorten(name[0]), name[0][0]] , [" ".join(name[1]), shorten(name[1])])

"""
load: 
	Takes in an file containing abstracts and titles on separate lines
"""
def load(filename):
	with open(filename) as f:
		holder = [i.strip().lower() for i in f]

		try:
			temp = [(holder[i], holder[i+1]) for i in range(0, len(holder), 2)]
		except:
			print("ERROR", holder)
			raise
		return temp

"""
stemFile:
	applies the snowball stemmer to a list of papers, stemming both abstracts and titles
"""
def stemFile(fileLst, spSet = {}):
	papers = []
	for paper in fileLst:
		try:
			papers.append((st.preprocess(paper[0], spSet), (st.preprocess(paper[1], spSet))))
		except:
			print(paper)
			raise

	stemmed = []
	for paper in papers:
		#title ,abs
		stemmed.append([[stemmer.stem(i) for i in paper[0][0]], [[stemmer.stem(word) for word in sentence] for sentence in paper[1]]\
			])
	#print("Preproc:", preproc[0][0][0])
	# untagged = [[[[tup[0] for tup in sentence] for sentence in component] for component in paper] for paper in preproc]
	# stemmed = [[[[stemmer.stem(word) for word in sentence] for sentence in component] for component in paper] for paper in untagged]
	return stemmed

def loadFile(filePath):
	with open(filePath) as f:
		holder = [i.strip().lower() for i in f]
	return holder