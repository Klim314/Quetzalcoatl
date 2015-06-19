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
import re

"""
getNames(filePath):
	Given a pubcrawl/pubdip output file, returns the two species terms encoded in the file name, as well as their 
	abbreviated forms

	Sample pubcrawl output file:
		Escherichia_coli#Pseudomonas_aeruginosa.compiled
		Escherichia_coli#Pseudomonas_aeruginosa.sp

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
	holder = []
	with open(filePath) as f:
		for i in f:
			holder.append(i.strip().lower())
	return holder

"""
tagStrip(line):
	removes the medline tag from the line

"""

def tagStrip(line):
	return line[6:]



"""""""""""""""""""""
#####################
#     .sp Files     #
#####################
"""""""""""""""""""""

"""
spFile():
	Class representation of a single .sp file. Contains the title, abstract, and their respective stemmed and tokenized forms

	loadSection(section):
		Loads a .sp section into split {TERM: DATA} dicitonaries.)
	
	readSpFile(spFIlePath):
		reads a SP file

	NOTE: Use as base class for all the other paper derivatives
	NOTE: For all future pubcrawl outputs, pmid is NECESSARY
"""
class spFile():
	def __init__(self, spFilePath):
		loaded = self.readSpFile(spFilePath)
		self.summary = self.loadSection(loaded["SUMMARY"])
		papers = loaded['PAPERS'].split('\n\n')
		self.papers = [self.loadSection(i) for i in papers]


	def loadSection(self, section):
		holder = [i.split("==") for i in section.split('\n') if i != '']
		result = {i:j.strip() for i,j in holder}
		return result


	def readSpFile(self, spFilePath):
		holder = {}
		with open(spFilePath) as f:
			for i in f:
				#find the first section
				if i[0] == '#':
					continue
				if i[0] == '@':
					current = i[1:].strip()
					holder[current] = ''
				else:
					holder[current] += i
		return holder

	#reads the list of papers, converts them into paper tuples
	def loadPapers(self, rawAbstractList):
		holder = []
		res = []
		for i in rawAbstractList:
			if i[0] == ">":
				if holder == []:
					holder = [i[2:]]
				else:
					res.append(holder)
					holder = [i[2:]]
			else:
				holder.append(i)
		return res
	def writeSpFile(self, filePath):
		with open(filePath, 'w') as f:
			#handle the summary
			f.write("@SUMMARY\n")
			for i in self.summary:
				f.write('== '.join([i, self.summary[i]]) + '\n')
			f.write("@PAPERS\n")
			for paperDict in self.papers:
				f.write("== ".join(["PMID", paperDict["PMID"]]) + "\n")
				f.write("== ".join(["AB  ", paperDict["AB  "]]) + "\n")
				f.write("== ".join(["TI  ", paperDict["TI  "]]) + "\n")
				f.write("== ".join(["TIHT", paperDict["TIHT"]]) + "\n")
				f.write("== ".join(["ABHT", paperDict["ABHT"]]) + "\n\n")





if __name__ == "__main__":
	target = '../formats_and_standards/sp_format_documentation.txt'
	outPath = '../formats_and_standards/tester/tester.sp'
	temp  = spFile(target)
	print(temp.papers)
	temp.writeSpFile(outPath)