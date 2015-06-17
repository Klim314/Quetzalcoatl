#!/usr/bin/env python3
from modules import sent_tokenize as st
from nltk.stem.snowball import SnowballStemmer
from modules import papers
from modules import modfile
import os
import evaluate
import re

"""
TODO

"""


"""
pattern.py
	Takes a paper file (.compiled) produced by pubcrawl, checks if any of the preloaded patterns are present. All members of patterns must be present and in order. 
	Patterns may be spaced out

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
	def __init__(self, title, abstract, spSet = {}):
		self.spSet = spSet
		self.title = title
		self.abstract = abstract
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

	paperSplit:
		takes a list of papers and converts them into a list of (Title, abstract) tuples. Currently discards any anomalous data
		TODO: Implement logging of discarded data
"""
class Pair():
	def __init__(self, filePath):
		#initalize the species sets
		sja, sjb = papers.getNames(filePath)[0], papers.getNames(filePath)[1]
		self.spSet1 = set(sja)
		self.spSet2 = set(sjb)
		self.spSet = self.spSet1.union(self.spSet2)

		#Load the papers
		self.rawPapers = papers.loadFile(filePath)
		self.papers = [Paper(i,j, self.spSet) for i,j in self.paperSplit(self.rawPapers) ]

	#Splits the papers into (Title, Abstract) 2-tuples
	def paperSplit(self, paperList):
		#Handle Missing Dat ahere
		holder, res = [], []
		for i in paperList:
			if i[:2] == "TI" or i[:2] == "ti":
				if holder == []:
					holder.append(i)
				elif len(holder) != 2:
					print("Warning: Erronous data detected")
					print(holder)
					holder = [i]
				else:
					res.append(holder)
					holder = [i]
			else:
				holder.append(i)

		if len(holder) != 2:
			print("Warning: Erronous data detected")
			print(holder)
		else:
			res.append(holder)
		return res	

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
		for regex in self.regexes:
			if regex.search(sentence):
				return True
		return False
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
				self.regexes.append(re.compile(".*".join(flags)))
				flags = self.text.split(' ')
		return
	def pCheck(self, paragraph):
		for sentence in paragraph:
			if self.check(sentence):
				return True
		return False

class nPattern():
	def __init__(textList):
		self.patterns = [Pattern(i)	for i in textList]

	def initialize(self, sja, sjb):
		for pattern in self.patterns:
			pattern.initialize(sja, sjb)

	def pCheck(self, paragraph):
		temp = [i for i in self.patterns]
		for pattern in self.patterns:
			if pattern.pCheck(paragraph):
				temp.remove(pattern)
		if len(temp) == 0:
			return True
		return False



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
	return sja+'#' + sjb + ".compiled"
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

	for paper in pairPapers.papers:
		
		if test(paper, patternList) or test(paper, reverseList):
			with open (outPath, 'a') as f:
				f.write(paper.title + '\n')
				f.write(paper.abstract + '\n')


def debug(filePath):
	names = papers.getNames(filePath)
	sja, sjb = names[0][0], names[1][0]
	patternList = makePatterns(patterns)
	reverseList = makePatterns(patterns)
	for pattern in patternList:
		pattern.initialize(sja, sjb)
	for pattern in reverseList:
		pattern.initialize(sjb, sja)

	paper = Paper("ti  - cocktails of probiotics pre-adapted to multiple stress factors are more robust under simulated gastrointestinal conditions than their parental counterparts and exhibit enhanced antagonistic capabilities against escherichia coli and staphylococcus aureus.", "ab  - background: the success of the probiotics in delivery of health benefits depends  on their ability to withstand the technological and gastrointestinal conditions; hence development of robust cultures is critical to the probiotic industry. combinations of probiotic cultures have proven to be more effective than the use of single cultures for treatment and prevention of heterogeneous diseases. we investigated the effect of pre- adaptation of probiotics to multiple stresses on their stability under simulated gastrointestinal conditions and the effect of their singular as well as their synergistic antagonistic effect against selected enteric pathogens. methods: probiotic cultures were inoculated into mrs broth adjusted to ph 2 and incubated for 2 h at 37 degrees c. survivors of ph 2 were subcultured into 2% bile acid for 1 h at 37 degrees c. cells that showed growth after exposure to 2% bile acid for 1 h were finally inoculated in fresh mrs broth and incubated at 55 degrees c for 2 h. the cells surviving were then used as stress adapted cultures. the adapted cultures were exposed to simulated gastrointestinal conditions and their non- adapted counterparts were used to compare the effects of stress adaptation. the combination cultures were tested for their antipathogenic effects on escherichia coli and staphylococcus aureus. results: acid and bile tolerances of most of the stress-adapted cells were higher than of the non-adapted cells. viable counts of all the stress-adapted lactobacilli and bifidobacterium longum lmg 13197 were higher after sequential exposure to simulated gastric and intestinal fluids. however, for b. longum bb46 and b. bifidum lmg 13197, viability of non-adapted cells was higher than for adapted cells after exposure to these fluids. a cocktail containing l. plantarum + b. longum bb46 + b. longum lmg 13197 best inhibited s. aureus while e. coli was best inhibited by a combination containing l. acidophilus la14 150b + b. longum bb46 + b. bifidum lmg 11041. a cocktail containing the six non- adapted cultures was the least effective in inhibiting the pathogens. conclusion: multi-stress pre-adaptation enhances viability of probiotics under simulated gastrointestinal conditions; and formulations containing a mixture of multi stress-adapted cells exhibits enhanced synergistic effects against foodborne pathogens.")
	temp = patternList[1].regexes
	temp2= reverseList[1].regexes
	target = paper.sAbstract[9]
	print(target)
	for i in temp:
		for j in temp2:
			print(i)
			print(i.search(target))
			print(j)
			print(j.search(target))
	print(paper.title)
	print(paper.sTitle)


if __name__ == "__main__":

	target = "input/pattern/tester/Lactobacillus_acidophilus#Escherichia_coli.compiled"
	#debug(target)
	execute(target)
	