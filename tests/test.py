import nltk
import re

_LINE_RE = re.compile('(\S+)\s+(\S+)\s+([IOB])-?(\S+)?')
with open("../input/chunktest.in") as f:
	holder = ''
	res = []
	for i in f:
		if i == '\n':
			res.append(holder)
			holder = ''
			continue
		holder += i

print(res[0])
def process(sentence):
	splat = [i for i in sentence.split('\n')]
	res = []

	#obtain the word, the POS tag and the chunk tag
	for i in splat:
		temp = i.split('\t')
		#print(temp)
		if temp == ['']:
			continue
		if temp[0] in [".", ',']:
			res.append([temp[0], temp[-2], temp[-1]])
		else:
			res.append([temp[0], temp[2], temp[3]])
		print (res)
	return "\n".join(['	'.join(i) for i in res])


"""
text3 = process(res[1])
nltk.chunk.conllstr2tree(text3).draw()