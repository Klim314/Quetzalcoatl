#!/usr/bin/env python3
from modules import paperparse as pp
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument( "target", help ="Target directory for evaluation")
parser.add_argument( "annotated", help ="Directory containing annotated files")
parser.add_argument( "-o", "--outdir", help ="Override output directory. Default = output/patternscan/evaluate/", default = "output/patternscan/evaluate/")
args = parser.parse_args()

trueHitDir = args.outdir + "true_hits/"
falseHitDir = args.outdir + "false_hits/"
missedHitDir = args.outdir + "missed_hits/"

if not os.path.exists(args.outdir) :
	os.makedirs(args.outdir)

if not os.path.exists(trueHitDir) :
	os.makedirs(trueHitDir)

if not os.path.exists(falseHitDir) :
	os.makedirs(falseHitDir)
	
if not os.path.exists(missedHitDir) :
	os.makedirs(missedHitDir)

if args.target[-1] != '/':
	args.target += '/'

if args.annotated[-1] != '/':
	args.annotated += '/'
print("Reading Directory")
tester = [args.target + i for i in sorted(os.listdir(args.target))]
annotated = [args.annotated + i for i in  sorted(os.listdir(args.annotated))]

holder = dict()

for i in tester:
	holder[os.path.basename(i).lower()] = [i]

for i in annotated:
	holder[os.path.basename(i).lower()].append(i)
	
totalPos = 0
totalNeg = 0

testerPos = 0
testerPosHit = 0
testerNeg = 0
testerNegHit = 0

for i in holder:
	temp = holder[i]
	testerPath = pp.spFile(temp[0])
	annPath = pp.spFile(temp[1])
	print(annPath.summary)
	print(testerPath.summary)
	print("----------------------")
	if annPath.summary["POS "].strip() == '1':
		totalPos += 1
	elif annPath.summary["POS "].strip() == '0':
		pass
	else:
		print("ERROR1: ", temp[1])

	if annPath.summary["NEG "].strip() == '1':
		totalNeg += 1
	elif annPath.summary["NEG "].strip() == '0':
		pass
	else:
		print("ERROR2: ", temp[1])

	if testerPath.summary["POS "].strip() == '1':
		testerPos += 1
		if annPath.summary["POS "].strip() == '1':
			testerPosHit +=1
	elif testerPath.summary["POS "].strip() == '0':
		pass
	else:
		print("ERROR3: ", temp[0])

	if testerPath.summary["NEG "].strip() == '1':
		testerNeg += 1
		if annPath.summary["NEG "].strip() == '1':
			testerNegHit +=1
			testerPath.writeSpFile(trueHitDir + testerPath.fileName)
		else:
			testerPath.writeSpFile(falseHitDir + testerPath.fileName)
	elif testerPath.summary["NEG "].strip() == '0':
		if annPath.summary["NEG "].strip() == "1":
			annPath.writeSpFile(missedHitDir + annPath.fileName)
	else:
		print("ERROR4: ", temp[0])
		print(annPath.summary)

print("TotalPos: ", totalPos)
print("TotalNeg: ", totalNeg)
print("testerPos",testerPos)
print("testerPosHit",testerPosHit)
print("testerNeg",testerNeg)
print("testerNegHit",testerNegHit)


