# Quetzalcoatl
This is the bacterial datamining package <NAME>

constituent scripts:
	CORE:
		pubcrawl
			Bioconductor-based abstract miner
		abcheck
			Coarse filter system for inhibitory relationships
		iob2tree
			creation of chunked text nltk trees
		<TO BE IMPLEMENTED>
		quetzalcoatl
			NLP-based fine filter for inhibitory relationships
		hermes:
			linker script for the entire Quetzacoatl system
	SUPPLEMENTARY:
		evaluate:
			Evaluation system for abcheck. Requires a preannotated data set
