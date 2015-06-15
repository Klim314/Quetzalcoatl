#!/usr/env/bin python3
import nltk
import pexpect
import os
"""
iob2tree:
	Takes a file containing a presplit paper (sent_tokenize.sentSplit <in abcheck>), chunks it using geniatagger and imports it as an nltk Tree

	input: File containing a sentences split by newlines

	output: a list of tree objects, one tree for each sentence in the abstract
"""


"""
sProc: preprocesses a given chunked sentence, coverting it into a nltk readable format
input: GENIAtagger chunked sentence
output: nltk IOB list
"""
def sProc(sentence):
	splat = [i for i in sentence.split('\n')]
	res = []
	#handle punctuation
	punct = [".", ',']

	#obtain the word, the POS tag and the chunk tag
	for i in splat:
		temp = i.split('\t')
		print(temp)
		if temp == ['']:
			continue

		if temp[0] in punct:
			res.append([temp[0], temp[-2], temp[-1]])
		else:
			res.append([temp[0], temp[2], temp[3]])
	return "\n".join(['	'.join(i) for i in res])

"""
abProc:
Applies sProc to all sentences in an abstract
"""
def abProc(senLst):
	result = [sProc(i) for i in senLst]
	return result

"""
chunk:
	Takes in a file containing a single abstract and chunks it using the
	GENIA tagger. 

	Input: File containing a single abstract, abstract must be broken into single
		sentence lines

	Note: GeniaTagger only runs from it's own directory thus the cwds.
"""
def chunk(targetFile):
	print("-----------")
	#escape the spaces in filenames
	targetFile = targetFile.replace(" ", "\ ")


	oriDir = os.getcwd()
	#set this directory to the geniatagger directory
	#geniatagger is required to be run from it's directory and cannot be accessed directly
	os.chdir("extparsers/geniatagger-3.0.1")
	child = pexpect.spawn("./geniatagger " +"../../" +  targetFile)
	child = [i for i in child]
	print(child)
	results = [i.decode("utf-8") for i in child[4:]]
	os.chdir(oriDir)
	return results
"""
senSplit:
	Takes chunked abstract, returns list of chunked sentences, one index per setence

"""
def senSplit(chunkLst):
	holder = ""
	result = []
	chunkLst = [i.strip() + '\n' for i in chunkLst]
	for i in chunkLst:
		if i == "\n":
			if holder != '':
				result.append(holder)
				holder = ''
			continue
		else:
			holder += i
	if holder != "":
		result.append(holder)

	return result
"""
execute:
	Overall execution function. Collects all functions above.

	Input: File containing a single abstract, abstract must be broken into single
		sentence lines

	Output: List of nltk trees comprising the entire abstract
"""
def execute(targetFile):
	chunks = chunk(targetFile)
	print(chunks)
	#process chunked files for import
	pChunks = abProc(senSplit(chunks))
	print(pChunks)
	mktree = nltk.chunk.conllstr2tree

	return [mktree(i) for i in pChunks]



if __name__ == "__main__":
	# outdir = "../output/iob2tree/"
	# if not os.path.exists(outdir):
	# 	os.mkdir(outdir)
	indir = "output/abcheck/"
	inp = indir + "lactobacillus acidophilus#escherichia coli/53.out"
	print(inp)
	# with open(inp) as f:
	# 	for i in f:
	# 		print(i)
	[i.draw() for i in execute(inp)]
	# blah = execute(inp)
	# blah[0].draw()





# with open("../input/chunktest.in") as f:
# 	holder = ''
# 	res = []
# 	for i in f:
# 		if i == '\n':
# 			res.append(holder)
# 			holder = ''
# 			continue
# 		holder += i

# chunks = chunk("../../input/testsentences.in")
# pchunks = abProc(senSplit(chunks))
# print(pchunks)
# mktree = nltk.chunk.conllstr2tree
# mktree(pchunks[0]).draw()

# print(chunk("../../input/testsentences.in"))
# tester = abProc(res)
# chunktest = sProc(chunk("../../input/testsentences.in")[0])
# print(chunktest)
# nltk.chunk.conllstr2tree(chunktest).draw()*