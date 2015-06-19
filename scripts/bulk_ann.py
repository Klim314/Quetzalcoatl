#!/usr/bin/env python3 
"""
bulk_ann.py: 
	Takes in a folder containing multiple pubcrawl output files. Converts them to the .sp annotation format

"""

import argparse
import os
import make_ann

parser = argparse.ArgumentParser()
parser.add_argument("target", help= "Path to directory containing pubcrawl output files")
parser.add_argument("-o", "--outDir", help= "Directory to output data to", default = 'output/ann_format/')
parser.add_argument("-t", "--terms", help= "Medline terms in the file. Separate terms with ':'", default = 'PMID:TI:AB')
args = parser.parse_args()

if args.target[-1] != '/':
	args.target += '/'

targets = [args.target + i for i in os.listdir(args.target)]
for i in targets:
	make_ann.execute(i, outDir = args.outDir, terms = args.terms)

