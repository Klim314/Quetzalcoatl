#!/usr/bin/env python3
"""
completeness.py
	Checks the data completeness of a particular pubcrawl output dataset
	Takes in the directory path, seed file and outputs a list of all missing species pairs
"""


import os
import sys

target = sys.argv[1]
seed = sys.argv[2]

holder = set()

for i in os.listdir(target):
	name = os.path.splitext(os.path.basename(i))[0]
	name = "\t".join(name.split("#"))
	name = " ".join(name.split("_"))
	holder.add(name)

with open (seed) as f:
	for i in f:
		if i.strip() not in holder:
			print(i.strip())



