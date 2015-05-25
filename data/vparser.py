#!/usr/bin/env python3
import nltk
from nltk.grammar import ProbabilisticProduction, Nonterminal
import xmltree
import sent_tokenize as st

#taken from http://bogdan-ivanov.com/training-a-simple-pcfg-parser-using-nltk/
class PCFGViterbiParser(nltk.ViterbiParser):
    def __init__(self, grammar, trace=0):
        super(PCFGViterbiParser, self).__init__(grammar, trace)
 
    @staticmethod
    def _preprocess(tokens):
        replacements = {
            "(": "-LBR-",
            ")": "-RBR-",
        }
        for idx, tok in enumerate(tokens):
            if tok in replacements:
                tokens[idx] = replacements[tok]
 
        return tokens
 
    @classmethod
    def train(cls, productions, root):
        pcfg = nltk.grammar.induce_pcfg(nltk.grammar.Nonterminal(root), productions)
        return cls(pcfg)
 
    def parse(self, tokens):
        #tokens = self._preprocess(list(tokens))
        tagged = nltk.pos_tag(tokens)
        # tagged = tokens
        # print(tagged)
        # tokens = [i[0] for i in tagged]
        # print("TOOOOKKENNSS-------------")
        # print(tokens)
 
        missing = False
        for tok, pos in tagged:
            if not self._grammar._lexical_index.get(tok):
                missing = True
                self._grammar._productions.append(ProbabilisticProduction(Nonterminal(pos), [tok], 
                                                                                prob=0.000001))
        if missing:
            self._grammar._calculate_indexes()

        print(self._grammar)
        return super(PCFGViterbiParser, self).parse(tokens)


f = "/home/esyir/Documents/A-star/NLP/data/GENIA_treebank_v1/10022882.xml"

tree = xmltree.analyze(f)
production = tree[0].productions()

S = nltk.Nonterminal('S')

grammar = nltk.induce_pcfg(S, production)

viterbi_parser = PCFGViterbiParser.train(production, 'S')
tokenized = st.preprocess("all of these results suggested that the slps of both l. acidophilus strains possessed murein hydrolase activities that were sublethal to e. coli cells.")

a123 = "all of these results suggested that the slps of both l. acidophilus strains possessed murein hydrolase activities that were sublethal to e. coli cells."





tokenized2 = tokenized[0] 

print(tokenized2)

print("BAM")
b123 = viterbi_parser.parse(tokenized2)
print([i for i in b123])


# testparser = nltk.parse.viterbi.ViterbiParser(grammar)
# #print(a123)
# print([i for i in testparser.parse(tokenized)])


 
# nltk.word_tokenize('Numerous passing references to the phrase have occurred in movies'))

# print t
