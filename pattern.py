#!/usr/bin/env python3
from modules import sent_tokenize as st
from nltk.stem.snowball import SnowballStemmer
from modules.papers import getNames, load, stemFile
from modules import modfile
import os
import evaluate

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
abb
	Takes in a string of format A B, where A is the genus and B the Species. Returns abbreviated species name
"""

def abb(spec):
	temp = spec.split(' ')
	return temp[0][0] + '. ' + temp[1]

"""
specJoin

"""

def specJoin(sentence, spSet):
	holder = []
	i = 0
	while i < len(sentence  )-1:
		if ' '.join([sentence[i], sentence[i+1]]) in spSet:
			holder.append(" ".join([sentence[i], sentence[i+1]]))
			i+=1
		else:
			holder.append(sentence[i])

		i+=1

	return holder

"""
test
	analyzes a tokenized, stemmed sentence for a relationship between species A and species B (sja, sjb)
	Positive depends on the 
"""

def test(compiled, tokStemSent, sja, sjb):
	for pattern in compiled:
		if pattern.check(tokStemSent, sja, sjb) or pattern.check(tokStemSent, sjb, sja):
			print("HIT", tokStemSent)
			return True
	return False

def paraTest(compiled, tokStemPara, sja, sjb):
	for sentence in tokStemPara:
		if(test(compiled, sentence, sja, sjb)):
			return True
	return False

"""
pattern:
	contains a string pattern to be checked against

"""

class pattern():
	def __init__(self, text):
		self.text = text
		
	#sentence is tokenized
	def check(self, sentence, sja, sjb):
		#set up the text with the name terms
		
		text = self.text.replace('sja', sja)
		ext = text.replace('sjb', sjb)
		spSet1 = set([sja, abb(sja)])
		spSet2 = set([sjb, abb(sjb)])
		spSet = spSet1.union(spSet2)
		flags = specJoin(st.specWordJoin(text.split(' ')), spSet)
		for i in range(len(flags)):
			if flags[i] == sja:
				flags[i] = spSet1
			elif flags[i] == sjb:
				flags[i] = spSet2
			else:
				flags[i] = [flags[i]]
		#print(flags)

		cur = 0
		end = len(flags)
		for i in sentence:
			# print(i)
			# print(flags[cur])
			# print("------------")
			try:
				if i in flags[cur]:
					cur+=1
					if cur == end:
						return True
			except:
				print("ERROR", i)
				raise
		return False

class nPattern():
	def __init__(self, textLst):
		self.patterns = textLst
		self.text = self.patterns
		self.holder = {i:0 for i in self.patterns}
		
	#sentence is tokenized
	def checkSingle(self, sentence, sja, sjb, pattern):
		#set up the text with the name terms
		text = pattern.replace('sja', sja)
		text = text.replace('sjb', sjb)
		spSet1 = set([sja, abb(sja)])
		spSet2 = set([sjb, abb(sjb)])
		spSet = spSet1.union(spSet2)
		flags = specJoin(st.specWordJoin(text.split(' ')), spSet)
		for i in range(len(flags)):
			if flags[i] == sja:
				flags[i] = spSet1
			elif flags[i] == sjb:
				flags[i] = spSet2
			else:
				flags[i] = [flags[i]]
		#print(flags)

		cur = 0
		end = len(flags)
		for i in sentence:
			# print(i)
			# print(flags[cur])
			# print("------------")
			try:
				if i in flags[cur]:
					cur+=1
					if cur == end:
						return True
			except:
				print("ERROR", i)
				raise
		return False
	def check(self, text, sja, sjb):

		for pattern in self.patterns:
			pass

		return False





"""
Constants and preloaded junk
"""
spSet = set()
with open("data/Species.txt") as f:
	for i in f:
		spSet.add(i.strip().lower())
		spSet.add(abb(i.strip().lower()))

stemmer = SnowballStemmer("english")

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

patterns = [st.preprocess(i)[0] for i in patterns]
patterns = [[stemmer.stem(j) for j in i ] for i in patterns]
patterns = [" ".join(i) for i in patterns]
compiled = [pattern(i) for i in patterns]

# nPatterns = [
# ["bacteriocin produced sjA", "inhibit sjB"]
# ]
# nPatterns = [[st.preprocess(i)[0] for i in j] for j in nPatterns]
# nPatterns = [[[stemmer.stem(i)for i in j] for j in k] for k in nPatterns]
# nPatterns = [[" ".join(i) for i in j] for j in nPatterns]
# compiled += [nPattern(i) for i in nPatterns]

print("------PATTERNS------")
[print(i.text) for i in compiled]
# print("nPatterns: ", nPatterns)
print("------PATTERNS------")

outDir = "output/pattern/"
if not os.path.exists(outDir):
	os.mkdir(outDir)

def execute(target):
	names = getNames(target)
	print("InFile: ", target)
	print(compiled[0].text)

	allP = load(target)
	oriP = load(target)

	stemmed = stemFile(allP, spSet)
	holder = []
	for (title, abstract), (oTitle, oAbstract) in zip(stemmed, oriP):
		if test(compiled, title, names[0][0], names[1][0]) or test(compiled, title, names[1][0], names[0][0]):
			holder.append((oTitle, oAbstract))
		elif paraTest(compiled, title, names[0][0], names[1][0]) or paraTest(compiled, title, names[1][0], names[0][0]):
			holder.append((oTitle, oAbstract))

	outFile = outDir + os.path.basename(os.path.splitext(target)[0]) + ".out"
	print("Outfile: ", outFile)
	if holder:
		with open(outFile, 'w') as f:
			for i in holder:
				f.write(i[0] + '\n')
				f.write(i[1] + '\n')
	return


if __name__ == "__main__":
	target = "input/pattern/smalltest/Lactobacillus_plantarum#Lactococus_lactis"
	names = getNames(target)
	# print("------TARGET NAMES------")
	# print(names)
	# print(names[0][0], names[1][0])
	# print("------TARGET NAMES------")
	allP = load(target)

	#print(allP)
	stemmed = stemFile(allP, spSet)

	#/////////////////////////
	#DEEEEEBBUUUUGGGG
	#//////////////////////


	# print("DEEEEEBBUUUUGGGG")
	# print("------------------")
	# strTest = stemmed[11][0]
	# strTest = ['murein', 'hydrolas', 'activ', 'of', 'surfac', 'layer', 'protein', 'from', 'lactobacillus acidophilus', 'against', 'escherichia coli', '.']
	# print(strTest)
	# # print([test(compiled, i,"lactobacillus acidophilus", "escherichia coli") for i in strTest])
	# print(test(compiled, strTest, "lactobacillus acidophilus", "escherichia coli"))
	execute(target)
	print("ENDED")
	raise


	#?///////////////////1
	#ENDDD DEEEEBUUUGGGG
	#//////////////
	holder = []
	for title, abstract in stemmed:
		if test(compiled, title, names[0][0], names[1][0]) or test(compiled, title, names[1][0], names[0][0]):
			holder.append("T")
		elif paraTest(compiled, title, names[0][0], names[1][0]) or paraTest(compiled, title, names[1][0], names[0][0]):
			holder.append("T")
		else:
			holder.append("F")
	print(holder)

	#EVALUTATION	
	annPath = "annotated/lactobacillus_acidophilus#escherichia_coli.ann"
	print("WITHOUT AMBIGUOUS/TITLE ONLY")
	evaluate.evaluate(holder, annPath, 1,  "testlog")
	print("WITH AMBIGUOUS/TITLE ONLY")
	evaluate.evaluate(holder, annPath, 0,  "testlog")



	# sentTest = "escherichia coli was found to compete with lactobacillus acidophilus"
	# sentTest = st.preprocess(sentTest, spSet)
	# sentTest = [stemmer.stem(i) for i in sentTest]
	# print("input: ", sentTest)

	# print(test(compiled, sentTest, "escherichia coli", "lactobacillus acidophilus"))