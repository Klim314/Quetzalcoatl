#!/usr/bin/env python3
import nltk
import numpy, matplotlib
text = """`You may want to repeat such calculations on several texts, but it is tedious to keep retyping the formula. Instead, you can come up with your own name for a task, like "lexical_diversity" or "percentage", and associate it with a block of code. Now you only have to type a short name instead of one or more complete lines of Python code, and you can re-use it as often as you like."""

bio = "The distribution, genome location, and evolution of the four paralogous zinc metalloproteases, IgA1 protease, ZmpB, ZmpC, and ZmpD, in Streptococcus pneumoniae and related commensal species were studied by in silico analysis of whole genomes and by activity screening of 154 representatives of 20 species. ZmpB was ubiquitous in the Mitis and Salivarius groups of the genus Streptococcus and in the genera Gemella and Granulicatella, with the exception of a fragmented gene in Streptococcus thermophilus, the only species with a nonhuman habitat. IgA1 protease activity was observed in all members of S. pneumoniae, S. pseudopneumoniae, S. oralis, S. sanguinis, and Gemella haemolysans, was variably present in S. mitis and S. infantis, and absent in S. gordonii, S. parasanguinis, S. cristatus, S. oligofermentans, S. australis, S. peroris, and S. suis. Phylogenetic analysis of 297 zmp sequences and representative housekeeping genes provided evidence for an unprecedented selection for genetic diversification of the iga, zmpB, and zmpD genes in S. pneumoniae and evidence of very frequent intraspecies transfer of entire genes and combination of genes. Presumably due to their adaptation to a commensal lifestyle, largely unaffected by adaptive mucosal immune factors, the corresponding genes in commensal streptococci have remained conserved. The widespread distribution and significant sequence diversity indicate an ancient origin of the zinc metalloproteases predating the emergence of the humanoid species. zmpB, which appears to be the ancestral gene, subsequently duplicated and successfully diversified into distinct functions, is likely to serve an important but yet unknown housekeeping function associated with the human host. IMPORTANCE: The paralogous zinc metalloproteases IgA1 protease, ZmpB, ZmpC, and ZmpD have been identified as crucial for virulence of the human pathogen Streptococcus pneumoniae. This study maps the presence of the corresponding genes and enzyme activities in S. pneumoniae and in related commensal species of the genera Streptococcus, Gemella, and Granulicatella. The distribution, genome location, and sequence diversification indicate that zmpB is the ancestral gene predating the evolution of today's humanoid species. The ZmpB protease may play an important but yet unidentified role in the association of streptococci of the Mitis and Salivarius groups with their human host, as it is ubiquitous in these two groups, except for a fragmented gene in Streptococcus thermophilus, the only species not associated with humans. The relative sequence diversification of the IgA1 protease, ZmpB, and ZmpD is striking evidence of differences in selection for diversification of these surface-exposed proteins in the pathogen S. pneumoniae compared to the closely related commensal streptococci."
in1 = """Intrageneric inhibition between strains of P. acnes occurred much more commonly than intergeneric inhibition between strains of P. acnes and Micrococcaceae, and more often than intrageneric inhibition between strains of
Micrococcacea"""
in2 = """Our unpublished data indicate that vaginal E. faecalis strains, if beta-hemolytic, are strongly antagonistic to most vaginal Lactobacillus species in vitro"""
tBio = nltk.sent_tokenize(bio)
tIn1 = nltk.sent_tokenize(in1)
tIn2 = nltk.word_tokenize(in2)

print(tBio)
