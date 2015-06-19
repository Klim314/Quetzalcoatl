#!/usr/bin/env python3
from modules import sent_tokenize as st
from nltk.stem.snowball import SnowballStemmer
from modules import papers
from modules import modfile
import os
import re
from modules import paperparse as pp


"""
pattern.py
	Takes an .sp file produced by pubcrawl, checks if any of the preloaded patterns are present. All members of patterns must 
	be present and in order. Patterns may be spaced out

ALL PATTERNS USED

Activity A against B

containing A inhibited B

A decreased B

bacteriocins A inhibit B

A compete B

Antagonistic A on B

A antimicrobial B

A antibacterial B

A antagonistic B

A bacteriocin against B

A inhibit B
"""
"""
GLOBALS
"""
#Word Stemmer
stemmer = SnowballStemmer('english')

#Output Directory
outDir = "output/pattern/"
if not os.path.exists(outDir):
	os.mkdir(outDir)

"""""""""""""""""""""
#####################
#      PATTERNS     #
#####################
"""""""""""""""""""""

#Single-line Patterns
patterns = ["Activity sjA against sjB",
"containing sjA inhibited sjB",
"sjA decreased sjB",
"bacteriocin sjA sjB",
"sjA compet sjB",
"Antagonistic sjA on sjB",
"sjA antimicrobial sjB",
"sjA antibacterial sjB",
"sjA antagonistic sjB",
"sjA bacteriocin sjB",
"sjA inhibit sjB",
"inhibit sjA by sjB"]



"""""""""""""""""""""
#####################
#       CLASSES     #
#####################
"""""""""""""""""""""

"""
Paper():
	Class representation of a single paper. Contains the title, abstract, and their respective stemmed and tokenized forms
"""
class Paper():
	def __init__(self, spFilePaper, spSet = {}):
		self.spSet = spSet
		self.title = spFilePaper["TI  "]
		self.abstract = spFilePaper["AB  "]
		self.sTitle = self.tokStem(self.title)
		self.sAbstract = self.tokStem(self.abstract)

	def tokStem(self, paragraph):
		temp = st.preprocess(paragraph, self.spSet)
		temp = [[stemmer.stem(i) for i in j] for j in temp]
		return [" ".join(i) for i in temp]

	def export(self):
		print("-------PAPER--------")
		print(self.spSet)
		print(self.title)
		print(self.abstract)
		print(self.sTitle)
		print(self.sAbstract)
		print("-------PAPER--------")

"""
Pair():
	Class contained of paper objects for all papers for a species pair. 
	Takes in a filePath to a set of line-separated, initalizer-tagged papers
	from that pair and packages them into Paper() objects


"""
class Pair():
	def __init__(self, filePath):
		#initalize the species sets
		sja, sjb = papers.getNames(filePath)[0], papers.getNames(filePath)[1]
		self.spSet1 = set(sja)
		self.spSet2 = set(sjb)
		self.spSet = self.spSet1.union(self.spSet2)

		#Load the papers
		self.spFile = pp.spFile(filePath)
		#unified is a tuple: (spFile.papers[i], Paper)
		self.unified = [(i, Paper(i, self.spSet)) for i in self.spFile.papers]

	def test(self, unifiedObject, patternList):
		flag = 0
		for pattern in patternList:
			titleCheck = pattern.pCheck(unifiedObject[1].sTitle)
			if titleCheck:
				unifiedObject[0]['TIHT'] += ":#:".join([i.group(0) for i in titleCheck])
				flag = 1
			abstractCheck = pattern.pCheck(unifiedObject[1].sAbstract)	
			if abstractCheck:
				unifiedObject[0]['ABHT'] += ":#:".join([i.group(0) for i in abstractCheck])
				flag = 1
		return flag
	def testAll(self, patternList, outPath):
		for unifiedObject in self.unified:
			isTrue = self.test(unifiedObject, patternList)
			if isTrue:
				self.spFile.summary["INT "] = '1'
			self.spFile.writeSpFileHits(outPath)


"""
pattern:
	Takes in a pattern sentence. Establishes a regex from the pattern and the initialization variables and uses it to detect informative patterns
	in the data.

	check(sentence):
		takes in a sentence and, using the precompiled regexes, attempts to detect a pattern. returns True if detected, false otherwise
	Initialize(sja, sjb):
		Compiles multiple regex variations of the pattern sentence from two input species


"""
class Pattern():
	def __init__(self, text):
		self.text = text
		self.regexes = []
	def check(self, sentence):
		holder = []
		for regex in self.regexes:
			temp = regex.search(sentence)
			if temp:
				holder.append(temp)
		return holder
	def initialize(self, sja, sjb):
		#cleanup
		self.regexes = []
		sja, sjb = sja.lower(), sjb.lower()

		sp1 = [sja, abb(sja)]
		sp2 = [sjb, abb(sjb)]

		flags = self.text.split(' ')
		for j in sp1:
			for k in sp2:
				for i in range(len(flags)):
					if flags[i] == "sja":
						flags[i] = j
					elif flags[i] == "sjb":
						flags[i] = k
					else:
						flags[i] = flags[i]
				self.regexes.append(re.compile("(" + ".*".join(flags) + ")"))
				flags = self.text.split(' ')
		return
	def pCheck(self, paragraph):
		holder = []
		for sentence in paragraph:
			temp = self.check(sentence)
			if temp:
				holder.extend(temp)
		return holder

class nPattern():
	def __init__(textList):
		self.patterns = [Pattern(i)	for i in textList]

	def initialize(self, sja, sjb):
		for pattern in self.patterns:
			pattern.initialize(sja, sjb)

	def pCheck(self, paragraph):
		temp = [i for i in self.patterns]
		holder = []
		for pattern in self.patterns:
			checkData = pattern.pCheck(paragraph)
			if checkData:
				holder.extend(checkData)
				temp.remove(pattern)
		if len(temp) == 0:
			return holder
		return []



"""
abb
	Takes in a string of format A B, where A is the genus and B the Species. Returns abbreviated species name
"""

def abb(spec):
	temp = spec.split(' ')
	return temp[0][0] + '. ' + temp[1]

"""
makeName
"""

def makeName(sja, sjb):
	sja = '_'.join(sja.split(" "))
	sjb = '_'.join(sjb.split(" "))
	return sja+'#' + sjb + ".sp"
"""
makePatterns(patternStringList):
	takes in a list of pattern strings and processes them (tokenizing, stemming) into Pattern objects
"""
def makePatterns(patternStringList):
	patterns = [st.preprocess(i)[0] for i in patternStringList]
	patterns = [[stemmer.stem(j) for j in i ] for i in patterns]
	patterns = [" ".join(i) for i in patterns]
	return [Pattern(i) for i in patterns]	

def test(paperObject, patternList):
	for pattern in patternList:
		if pattern.pCheck(paperObject.sTitle) or pattern.pCheck(paperObject.sAbstract):
			return True
	return False

"""
execute(filePath):
	Summary script. Loads all papers in the filepath and tests them with the preloaded patternStringList.
	TODO:
		allow customization of output folder
"""

def execute(filePath, postOutDir = ""):
	#Extraction of subject names
	names = papers.getNames(filePath)
	sja, sjb = names[0][0], names[1][0]
	#Creation of 
	if postOutDir != "" and postOutDir[-1] != "/":
		postOutDir += "/"
	outPath = outDir + postOutDir + makeName(sja, sjb)

	patternList = makePatterns(patterns)
	reverseList = makePatterns(patterns)
	for pattern in patternList:
		pattern.initialize(sja, sjb)
	for pattern in reverseList:
		pattern.initialize(sjb, sja)



	pairPapers = Pair(filePath)

	pairPapers.testAll(patternList, outPath)
	pairPapers.testAll(reverseList, outPath)
	# pairPapers.testAll(reverseList)

	# for paper in pairPapers.papers:
	# 	if test(paper, patternList) or test(paper, reverseList):
	# 		with open (outPath, 'a') as f:
	# 			f.write(paper.title + '\n')
	# 			f.write(paper.abstract + '\n')


def debug(filePath):
	names = papers.getNames(filePath)
	sja, sjb = names[0][0], names[1][0]
	patternList = makePatterns(patterns)
	reverseList = makePatterns(patterns)
	for pattern in patternList:
		pattern.initialize(sja, sjb)
	for pattern in reverseList:
		pattern.initialize(sjb, sja)
	Pair(filePath)


if __name__ == "__main__":

	target = "input/pattern/smalltestann/Lactobacillus_acidophilus#Escherichia_coli.sp"
	#debug(target)
	execute(target)
	