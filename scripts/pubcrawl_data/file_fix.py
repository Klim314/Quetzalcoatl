#!/usr/bin/env python3
import os


def load(fileName):
	with open(fileName) as f:
		holder = [i for i in f]
	return holder

def check(fileLst):
	holder = []
	result = []
	for i in fileLst:

		if i[:4] == "TI  ":
			if holder == []:
				holder.append(i)
			elif len(holder) !=2:
				print("MISSING DATA", holder)
				holder = []
				holder.append(i)
			else:
				result.append(holder)
				holder = []
				holder.append(i)
		elif i[:4] == "AB  ":
			holder.append(i)

	if len(holder) < 2:
		print("MISSING DATA", holder)
	else:
		result.append(holder)
	return sum(result, [])

def execute(fileName):
	holder = load(fileName)
	return check(holder)


if __name__ == "__main__":
	target = "../../input/pattern/2015-06-12-16_49/odd/Escherichia_coli#Enterococcus_faecalis.compiled"
	a = execute(target)
	print("-------------")
	check(a)
	print("Original Length: ", len(load(target)))
	print("Final Length: ", len(a))