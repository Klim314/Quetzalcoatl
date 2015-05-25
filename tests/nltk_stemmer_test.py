import nltk
from segtok.segmenter import split_single as ssplit
import re

sCheck = re.compile(r"( [a-zA-Z]\.)")
sWordCheck = re.compile(r"([a-zA-Z]\.)")

def specJoin(lst):
	new = []
	i = 0
	while i < len(lst):
		print(lst[i][-3:])
		if sCheck.match(lst[i][-3:]):
			new.append(lst[i] + ' ' + lst[i+1])
			i+=1

		else:
			new.append(lst[i])
		i+=1
	return new

def specWordJoin(lst):
	new = []
	i = 0
	while i < len(lst):
		if len(lst[i]) == 2 and sWordCheck.match(lst[i]):
			new.append(lst[i] + ' '+ lst[i+1])
			i+=1

		else:
			new.append(lst[i])
		i+=1
	return new


def preprocess(doc):
	sent = list(ssplit(doc))
	sent = specJoin(sent)
	#return sent
	sent = [nltk.word_tokenize(i) for i in sent]
	sent = [specWordJoin(i) for i in sent]
	sent = [nltk.pos_tag(i) for i in sent]
	return sent

wordnet = nltk.corpus.wordnet
a   = ["Antagonises", "Antagonise", "Antagonizes", "inhibits", "inhibiting", "Inhibition", "inhibitory","outcompeted","lethal", "sublethal", "KILLING","kills","predator","anticorrelated","lysed", "lyses", "competing", "competition", "competed", "suppressed", "decrease", "lowered", "bacteriocin"]
b = "all of these results suggested that the slps of both l. acidophilus strains possessed murein hydrolase activities that were sublethal to e. coli cells."
c = nltk.word_tokenize(b)
wn = nltk.stem.WordNetLemmatizer()
sn = nltk.stem.snowball.EnglishStemmer()

print("SN STEM: ",[sn.stem(i) for i in a])
print("WN STEM: ",[wn.lemmatize(i) for i in a])
# print("SN STEM: ",[sn.stem(i) for i in c])
# print("WN STEM: ",[wn.lemmatize(i) for i in c])

synsets = [wordnet.synsets(i) for i in a]
similar = [i[0].lemma_names() if i else None for i in synsets]
print(similar)

print(sn.stem(similar[2][1]))