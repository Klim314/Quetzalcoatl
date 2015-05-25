#!/usr/bin/env python3
import nltk
import xml.etree.ElementTree as ET
from nltk.grammar import ProbabilisticProduction, Nonterminal
from segtok.segmenter import split_single as ssplit

f = "/home/esyir/Documents/A-star/NLP/data/GENIA_treebank_v1/10022882.xml"


def getArticle(f):
	tree = ET.parse(f)
	root = tree.getroot()
	while root.tag != "MedlineCitation":
		print (root.tag, root.attrib)
		for child in root:
			print('#', child.tag, child.attrib)
		root = root[0]
	article = root[1]
	title = article[0]
	abstract = article[1][0]
	return (title, abstract)

article = getArticle(f)

print(article[0])

def sent2tree(node):
	trees = [sent2tree(i) for i in node]
	if node.tag == "tok":
		return nltk.Tree(node.attrib["cat"], [node.text])
	elif node.tag == "cons":
		return nltk.Tree(node.attrib["cat"], trees)
	else:
		return sent2tree(node[0])

def analyze(filename):
	article = getArticle(filename)
	return [sent2tree(article[0]), [sent2tree(i) for i in article[1]]]