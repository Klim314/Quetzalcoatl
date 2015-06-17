#!/usr/bin/env python3
"""
data_check
	Analyzes all pubcrawl output files within a folder. Checks for 0 size files and files with odd numbers of lines. Option to fix files is provided.
	0 size files are deleted, odd lined' file are moved to a "odd" folder by default
"""

import argparse
import os
import file_fix as fixer

parser = argparse.ArgumentParser()

parser.add_argument("folder", help = "Target folder")
parser.add_argument("-f", "--fix", help = "Fix flag. Odd lined files have aberrant data removed.", default = False, action = 'store_true')

args = parser.parse_args()

split = os.path.split(args.folder)

pref = split[0]

fileName = split[1]

oddDir = args.folder + "odd/"
if not os.path.exists(oddDir):
	os.makedirs(oddDir)

def isEmpty(fileName):
	if os.stat(fileName).st_size == 0:
		return True
	return False

def isOdd(integer):
	if integer%2 == 0:
		return False
	return True

def lineCount(file):
	holder = 0
	with open(file) as f:
		for i in f:
			holder+= 1
	return holder



for i in os.listdir(args.folder):
	fName = args.folder + i 
	if not os.path.isfile(fName):
		continue
	if isEmpty(fName):
		os.remove(fName)
	elif isOdd(lineCount(fName)):
		holder = fixer.execute(fName)
		print("MOVING: ", fName)
		os.rename(fName, oddDir + i)
		print("Writing", fName)
		with open(fName, 'w') as f:
			for i in holder:
				f.write(i)
		print('-------------')

