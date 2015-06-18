#!/usr/bin/env python3

"""
paperparse.py
	A set of functions to deal with pubcrawl data

"""

import nltk
import os
from segtok.segmenter import split_single as ssplit
try:
	from modules import sent_tokenize as st
except:
	import sent_tokenize as st

"""
getNames(filePath):
	Given a pubcrawl/pubdip output file, returns the two species terms encoded in the file name, as well as their 
	abbreviated forms

	Sample pubcrawl output file:
		Escherichia_coli#Pseudomonas_aeruginosa.compiled

	Resultant getNames output:
		[['escherichia coli', 'e. coli', 'escherichia'], ['pseudomonas aeruginosa', 'p. aeruginosa', 'pseudomonas']]
"""
def getNames(filePath):	
	def shorten(tup):
		return tup[0][0] + '. ' + tup[1]
	filePath = os.path.basename(filePath)
	name = os.path.splitext(filePath)[0]
	
	# print(name)
	name = [i.split('_') for i in name.split('#')]
	name = [[i.lower() for i in j] for j in name]
	#check if genus only
	# print(name)
	if len(name[0]) ==1:
			return [[i[0]] for i in name]

	return [[" ".join(i), shorten(i), i[0]] for i in name] 

"""
loadFile(filepath):
	generic file input. Takes in the file as raw data and returns a list of stripped and lowered lines.
"""

def loadFile(filePath):
	with open(filePath) as f:
		holder = [i.strip().lower() for i in f]
	return holder

"""
tagStrip(line):
	removes the medline tag from the line

"""

def tagStrip(line):
	return line[6:]
