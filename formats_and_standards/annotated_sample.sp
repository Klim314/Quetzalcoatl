#
# '@' signs define sectionbreaks 
# '#' signs define comments
# '>' signs define paper data modules
#
#ANNOTATION FORMAT
@BEGIN::SUMMARY
#Do the two species interact?
INTERACTS == 1
#is the interaction Positive?
POSITIVE == 0
#is the interaction Negative?
NEGATIVE == 1

@BEGIN::ABSTRACTS
#Individual papers broken up with >, followed by a pubmed ID
>PMID == 123456
#Title of the paper
TI == detection, partial purification and characterization of bacteriocin produced by lactobacillus brevis fptlb3 isolated from freshwater fish: bacteriocin from lb. brevis fptlb3.
#abstract that was analysed
AB == lactobacillus brevis fptlb3 was isolated from freshwater fish, capable of producing bacteriocin that had broad spectrum of inhibition (3200 au/ml) against escherichia coli mtcc 1563, enterococcus faecalis mtcc 2729, lactobacillus casei mtcc 1423, lactobacillus sakei atcc 15521 and staphylococcus aureus atcc 25923. the antimicrobial activity of crude supernatant fluid was stable after heating at 121 degrees c for 60 min and declined thereafter. stability of antimicrobial activity was observed at ph range of 2.0 to 8.0. its active principle was proteinaceous in nature since the bacteriocin was inactivated by proteolytic enzymes, but not by other non-proteolytic enzymes. mitomycin c and uv light did not affect the activity of the bacteriocin, while chloroform extraction completely destroyed their activity. exposure to surfactant resulted in an increase in titre, except nonidet p-40, which led to total loss of activity. no bacteriocin adsorption was detected at ph 1 to 2, whereas 100% bacteriocin adsorption was found at ph 6.5. based on tricine sds-page the estimated molecular mass of bacteriocin was 54 kda. no plasmid was found to present in the isolate.
#Portion of the title that matched the pattern, if any. (Not required for manual annotation)
TIHIT == 
#Portion of the abstract that matched the pattern, if any. If more than one is present, separate them with ':#:'. (Not required for manual annotation)
ABHIT == 

#Empty lines between entries are permissible. ###DEVNOTE###: Account for that in inputs

#Repeat for all Papers
>PMID == 123456
#Title of the paper
TI == detection, partial purification and characterization of bacteriocin produced by lactobacillus brevis fptlb3 isolated from freshwater fish: bacteriocin from lb. brevis fptlb3.
#abstract that was analysed
AB == lactobacillus brevis fptlb3 was isolated from freshwater fish, capable of producing bacteriocin that had broad spectrum of inhibition (3200 au/ml) against escherichia coli mtcc 1563, enterococcus faecalis mtcc 2729, lactobacillus casei mtcc 1423, lactobacillus sakei atcc 15521 and staphylococcus aureus atcc 25923. the antimicrobial activity of crude supernatant fluid was stable after heating at 121 degrees c for 60 min and declined thereafter. stability of antimicrobial activity was observed at ph range of 2.0 to 8.0. its active principle was proteinaceous in nature since the bacteriocin was inactivated by proteolytic enzymes, but not by other non-proteolytic enzymes. mitomycin c and uv light did not affect the activity of the bacteriocin, while chloroform extraction completely destroyed their activity. exposure to surfactant resulted in an increase in titre, except nonidet p-40, which led to total loss of activity. no bacteriocin adsorption was detected at ph 1 to 2, whereas 100% bacteriocin adsorption was found at ph 6.5. based on tricine sds-page the estimated molecular mass of bacteriocin was 54 kda. no plasmid was found to present in the isolate.
#Portion of the title that matched the pattern, if any. (Not required for manual annotation)
TIHIT == 
#Portion of the abstract that matched the pattern, if any. (Not required for manual annotation)
ABHIT == 