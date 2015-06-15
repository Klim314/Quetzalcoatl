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
    parser.add_argument("-c", "--cores", help= "Number of cores to use (default 4)", type = int, default = 4)
    args = parser.parse_args()

    target = args.target
    cores = args.cores
    files = [target + i for i in os.listdir(target) ]
    files = filter (os.path.isfile, files)
    with multiprocessing.Pool(cores) as pool:
        pool.map(pattern.execute, files)