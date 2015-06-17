#!/usr/bin/env python3
"""
sample.py
	Randomly samples a folder for filenames without replacement. Returns N paths to the specified files.
"""

import argparse
import os
import random
import shutil

def sample(dirPath, n):
	files = [dirPath + i for i in os.listdir(dirPath)]	
	if n > len(files):
		print("ERROR: sample size larger than total number of files")
		print("Filecount: ", len(files))
		raise 
	elif n > len(files)/2:
		print("Warning: sample size > 50% of the population")

	files = [i for i in files if os.path.isfile(i)]
	random.shuffle(files)
	return files[:n]

def copy(fileLst, outDir):
	if outDir[-1] != "/":
		outDir += "/"
	if not os.path.exists(outDir):
		os.makedirs(outDir)
	for i in fileLst:
		shutil.copyfile(i, outDir + os.path.basename(i))



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("target", help= "Directory containing files to be sampled. Must be in format {DirectoryName}/")
	parser.add_argument("samples", help= "Number of samples to take.", type = int)
	parser.add_argument("-c", "--copy", help = "Copy sampled files to an output folder")
	args = parser.parse_args()

	samples = sample(args.target, args.samples)
	if not args.copy:
		[print(i) for i in samples]
	else:
		copy(samples, args.copy)


