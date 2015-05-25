#!/usr/bin/env python3
"""
abcheck:
	Coarse filter system for inhibitory relationships
	Analyzes abstracts on a sentence by sentence basis searching for two stipulated terms and a 
	set of negative terms.
	
	Object A and B are each two letter names defined in the file name as follows
		OBJECT_A#OBJECT_B
	
	Input file is a file as follows:
		TI  - <TITLE TEXT>
		AB  - <ABSTRACT TEXT>
"""
#NOTE: Grab pre/proceeding sentences as well. Context

import nltk
import os
from segtok.segmenter import split_single as ssplit
from data import sent_tokenize as st
import evaluate


#////////////////////////
#INITIAL SETUP
#////////////////////////
if not os.path.exists("output/abcheck"):
	os.mkdir("output/abcheck")

outdir = "output/abcheck/"

"""
Negative terms and stemmer system
"""
unstemmed = ["Antagonistic","Antagonises", "Antagonise", "Antagonizes", "inhibits", "inhibiting", "Inhibition", "inhibitory",\
	"outcompeted","lethal", "sublethal", "KILLING","kills","predator","anticorrelated","lysed", "lyses", "competing", "competition",\
	 "competed", "suppressed", "decrease", "lowered", "bacteriocin", "reduced", "bacteriocin", "bacteriocins", "against", "reduced",\
	 "antibacterial", "viability"]
stemmer = nltk.stem.snowball.EnglishStemmer()
negTerm = [stemmer.stem(i) for i in unstemmed]
negTerm = set(negTerm)

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
	print(name)
	name = [i.split('_') for i in name.split('#')]
	#check if genus only
	print(name)
	if len(name[0]) ==1:
			return [i[0] for i in name]

	return [[" ".join(i), shorten(i), i[0]] for i in name] 

		#([" ".join(name[0]), shorten(name[0]), name[0][0]] , [" ".join(name[1]), shorten(name[1])])

"""
load: 
	Takes in an file containing abstracts and titles on separate lines
"""
def load(filename):
	with open(filename) as f:
		holder = []
		for i in f:
			#trim the 6 letter initalizer
			holder.append(i.strip().lower()[6:])
		return[(holder[i], holder[i+1]) for i in range(0, len(holder), 2)]



###TESTER
#returns a list of papers
#compirised of [TI, AB]
#where TI is list of str (sentence)
#and AB a list of sentences
#whcih are a list of strings
#[PAPER, PAPER] -> [TI, ABS] -> [SENT SENT] -> [WORD, WORD]

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

# Check if a term from all three required categories is in the sentence
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

def abcheck(abstract, spSet1, spSet2):
	b1, b2, d1, d2 = 0,0,0,0
	#DB raisees sensitivity but drastically drops specifiicity
	#Try forcing farness [] gap >3 tokens 
	db = 0
	for sentence in abstract:
		#check combinations on a per-sentence basis
		#b1, b2, negterm
		temp = [0,0,0]
		for word in sentence:
			if word in spSet1:
				temp[0] = 1
			elif word in spSet2:
				temp[1] = 1
			elif word in negTerm:
				temp[2] = 1
		print(temp)

		if temp == [1,1,1]:
			return True
		if temp == [1,0,1]:
			d1 = 1
		elif temp == [0,1,1]:
			d2 = 1
		elif temp == [1,0,0]:
			b1 = 1
		elif temp == [0,1,0]:
			b2 = 1
		#DB raisees sensitivity but drastically drops specifiicity
		elif temp == [1,1,0]:
			db = 1
	if b1 and d2 or b2 and d1 or d1 and d2: #db and b1 or db and b2 or
		return True
	return False
#all possible combs
#b1 d2
#b2 d1
#db b1/b2
#d1 d2
#
#
#



# def check(paper):
def execute(target):
	def write(enumPair, names):
		path = outdir + '#'.join(names) + '/' 
		if not os.path.exists(path):
			os.mkdir(path)
		print(path +  str(enumPair[0])+".out")
		with open(outdir + '#'.join(names) + '/' + str(enumPair[0])+".out", 'w') as f:
			f.write(enumPair[1][0] + "\n")
			temp = st.sentSplit(enumPair[1][1])

			[f.write(i + "\n") for i in temp]


	papers = load(target)
	orig = [i for i in papers]

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
	output = open(outdir + "abcheck.out", "w")
	holder = []	
	for original, paper in zip(enumerate(orig), stemmed):

		
		#Title fufills criteria
		if sheck(paper[0], spSet1, spSet2):
			holder.append("T")
			write(original, names)
			continue

		#Abstract fufills criteria
		if abcheck(paper[1], spSet1, spSet2):
			holder.append("T")
			write(original, names)
		else:
			holder.append("F")






if __name__ == "__main__":
	

	target = "input/lactobacillus_acidophilus#escherichia_coli.compiled"
	target = "input/Actinomyces#Bacteroides.compiled"
	execute(target)
	# raise
	# aoe = 3

	# #set of all stemmed negative terms
	# unstemmed = ["Antagonistic","Antagonises", "Antagonise", "Antagonizes", "inhibits", "inhibiting", "Inhibition", "inhibitory",\
	# "outcompeted","lethal", "sublethal", "KILLING","kills","predator","anticorrelated","lysed", "lyses", "competing", "competition",\
	#  "competed", "suppressed", "decrease", "lowered", "bacteriocin", "reduced", "bacteriocin", "bacteriocins", "against", "reduced",\
	#  "antibacterial", "viability"]
	# stemmer = nltk.stem.snowball.EnglishStemmer()
	# negTerm = [stemmer.stem(i) for i in unstemmed]
	# negTerm = set(negTerm)
	# print(negTerm)	
	# papers = load(target)
	# ori = [i for i in papers]


	# #set up sets of bacterial species
	# names = getNames(target)
	# print(names)
	# spSet1 = set(names[0])
	# spSet2 = set(names[1])
	# spSet = spSet1.union(spSet2)
	# #Load all papers 
	# allP = load(target)
	# #stem all papers
	# stemmed = stemFile(allP, spSet)

	# holder = []

	# #########DEBUG
	# # print('DEEEBUUUUGGG------------')
	# # paper1 = stemmed[270]
	# # print(paper1)
	# # print(abcheck(paper1[1], spSet1, spSet2))
	# # raise	
	# ###########END
	# output = open("output/output.out", "w")
	
	# for original, paper in zip(ori, stemmed):

		
	# 	# if sheck(paper[0], spSet1, spSet2) or any([sheck(i, spSet1, spSet2) for i in paper[1]]):
	# 	# 	holder.append("T")
	# 	# else:*
	# 	# 	holder.append("F")
	# 	if sheck(paper[0], spSet1, spSet2):
	# 		holder.append("T")
	# 		output.write(original[0] + "\n")
	# 		output.write(original[1] + "\n")
	# 		continue

	# 	#ABCHECK VARIANT
	# 	if abcheck(paper[1], spSet1, spSet2):
	# 		holder.append("T")
	# 		output.write(original[0] + "\n")
	# 		output.write(original[1] + "\n")
	# 	else:
	# 		holder.append("F")

	# output.close()
		#NAIV1E VARIANT
	# 	flag =0
	# 	for i in range(len(paper[1]) - aoe):
	# 		if sheck(sum(paper[1][i:i+aoe], []), spSet1, spSet2):
	# 			flag = 1

	# 	if flag:
	# 		holder.append("T")
	# 	else:
	# 		holder.append("F")


	#EVALUTATION	
	# annPath = "annotated/lactobacillus_acidophilus#escherichia_coli.ann"
	# evaluate.evaluate(holder, annPath,  "testlog")

	# print(holder)



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
