#!/usr/bin/env python3

"""
patternScan.py
    application of pattern.py to a set of input files
"""

import pattern
import os
import multiprocessing
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help= "Directory containing all files", default = "input/pattern/")
    parser.add_argument("-o", "--output", help= "Directory to output data to", default = "")
    parser.add_argument("-c", "--cores", help= "Number of cores to use (default 4)", type = int, default = 4)
    args = parser.parse_args()

    outDir = "output/pattern/" + args.output
    if outDir[-1] != '/':
        outDir += '/'
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    target = args.target
    cores = args.cores
    files = [target + i for i in os.listdir(target) ]
    files = filter (os.path.isfile, files)
    files = [(i, args.output) for i in files]
    with multiprocessing.Pool(cores) as pool:
       pool.starmap(pattern.execute, files)