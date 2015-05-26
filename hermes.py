#!#!/usr/env/bin python3
"""
hermes:
	interaction node of Quetzacoatl system
"""

import abcheck
import os
import iob2tree as i2tree



if __name__ == "__main__":
	target = "input/"
	acOutDir = "output/abcheck/"
	files = [target + i for i in os.listdir(target) ]
	files = filter (os.path.isfile, files)
	#print([i for i in files])
	for i in files: 	
		abcheck.execute(i)
	acOut = list(filter(os.path.isdir, [acOutDir + i for i in os.listdir(acOutDir)] ))
	"""
	NLP LOOP
	i2tree.execute imports the split files, converts them to trees for parsing and understanding by Quetzacoatl
	"""
	holder = []
	fro pair in acOut:
		for paper in os.listdir(pair):
			print("Chunking: ", paper)
			holder.append(i2tree.execute(paper))
			
