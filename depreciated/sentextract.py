#!/usr/bin/env python3
#Analyzes sentences for a sentence containing both object A and object B
# Object A and B are each two letter names defined in the file name as follows
# OBJECT_A_OBJECT_B
# Input file is a file as follows:
# TI  - <TITLE TEXT>
# AB  - <ABSTRACT TEXT>
# AOE MUST BE ODD

#NOTE: Grab pre/proceeding sentences as well. Context

import nltk
import os
from segtok.segmenter import split_single as ssplit
from data import sent_tokenize as st
import evaluate

#working in lowercase to make life easier
def getNames(file):	
	def shorten(tup):
		return tup[0][0] + '. ' + tup[1]
	file = os.path.basename(file)
	name = os.path.splitext(file)[0]
	print(name)
	name = [i.split('_') for i in name.split('#')]
	return [[" ".join(i), shorten(i), i[0]] for i in name] 

		#([" ".join(name[0]), shorten(name[0]), name[0][0]] , [" ".join(name[1]), shorten(name[1])])

def load(filename):
	with open(filename) as f:
		holder = []
		for i in f:
			#trim the 6 letter initalizer
			holder.append(i.strip().lower()[6:])
		return[(holder[i], holder[i+1]) for i in range(0, len(holder), 2)]

#debugging settings
target = "lactobacillus_acidophilus#escherichia_coli.compiled"
aoe = 3

#set of all stemmed negative terms
unstemmed = ["Antagonsises", "inhibits", "outcompeted", "out-competed",	"lethal","kills","predator","anticorrelated","lysed","decrease", "reduced", "competes", "activity", "growth", "competiton"]
stemmer = nltk.stem.snowball.EnglishStemmer()
negTerm = [stemmer.stem(i) for i in unstemmed]
negTerm = set(negTerm)
print(negTerm)	
papers = load(target)


###TESTER
#returns a list of papers
#compirised of [TI, AB]
#where TI is list of str (sentence)
#and AB a list of sentences
#whcih are a list of strings
#[PAPER, PAPER] -> [TI, ABS] -> [SENT SENT] -> [WORD, WORD]
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

# Check sentence for searched terms
def sheck(sentence, spSet1, spSet2):
	b1,b2, neg= 0,0,0
	for word in sentence:

		if word in spSet1:
			b1 = 1
		elif word in spSet2:
			b2 = 1
		elif word in negTerm:
			neg = 1
	if b1 and b2 and neg:
		return True
	return False

# def check(paper):
def execute():
	pass


#set up sets of bacterial species
names = getNames(target)
print(names)
spSet1 = set(names[0])
spSet2 = set(names[1])
spSet = spSet1.union(spSet2)
#Load all papers 
allP = load(target)
#stem all papers
stemmed = stemFile(allP, spSet)

holder = []
for paper in stemmed:

	
	# if sheck(paper[0], spSet1, spSet2) or any([sheck(i, spSet1, spSet2) for i in paper[1]]):
	# 	holder.append("T")
	# else:
	# 	holder.append("F")
	if sheck(paper[0], spSet1, spSet2):
		holder.append("T")
		continue

	flag =0
	for i in range(len(paper[1]) - aoe):
		if sheck(sum(paper[1][i:i+aoe], []), spSet1, spSet2):
			flag = 1

	if flag:
		holder.append("T")
	else:
		holder.append("F")
annPath = "annotated/lactobacillus_acidophilus#escherichia_coli.ann"
evaluate.evaluate(holder, annPath,  "testlog")

#print(holder)



# art1 = stemFile(allP, spSet)[0]
# print(art1)
# print(sheck (art1[0], spSet1, spSet2))





















# print(paper)
# # print("STOPs")
# stemmed_papers = stemFile(papers)
# # print(stemmed_papers)

# title = stemmed_papers[0][0][0]
# print(" ".join(title))
# print(title)
# print(sheck(title, spSet1, spSet2))





# names = getNames(target)
# first = [names[0].lower(), abb(names[0])]
# second = [names[1].lower(), abb(names[1])]

# with open(target) as f:
# 	for i in f:
# 		holder.append(i.lower())
# #group them into title, abstract sublists
# res = [(holder[i], holder[i+1]) for i in range(0, len(holder), 2)]

# sRes = []
# #tokenize and analyze each one
# for i,j in res:
# 	#tAb = nltk.sent_tokenize(j)
# 	tAb = [ i for i in ssplit(j)]
	

	
# 	for i in  range(len(tAb)):
# 		if i <aoe or i + aoe >= len(tAb):
# 			continue
# 		sentence = '\n'.join(tAb[i-aoe:i+aoe+1])
# 		if (first[0] in sentence or first[1] in sentence) and (second[0] in sentence or second[1] in sentence):
# 			sRes.append(sentence)

# #print(res[0])

# #print(res[1][1])
# [print(i + '\n\n-------------------') for i in sRes]
