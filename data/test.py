import nltk

grammar1 = nltk.CFG.fromstring("""
  S -> NP VP
  VP -> V NP | V NP PP
  PP -> P NP
  V -> "saw" | "ate" | "walked"
  NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
  Det -> "a" | "an" | "the" | "my"
  N -> "man" | "dog" | "cat" | "telescope" | "park"
  P -> "in" | "on" | "by" | "with"
  """)

rd = nltk.parse.Recursive
a = "By coculturing B. bacteriovorus 109J and M. aeruginosavorus ARL-13 with selected pathogens, we have demonstrated that predatory bacteria are able to attack bacteria from the genus Acinetobacter, Aeromonas, Bordetella, Burkholderia, Citrobacter, Enterobacter, Escherichia, Klebsiella, Listonella, Morganella, Proteus, Pseudomonas, Salmonella, Serratia, Shigella, Vibrio and Yersinia."