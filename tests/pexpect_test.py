import pexpect
import os


curdir = os.getcwd()
#set this directory to the geniatagger directory
#geniatagger is required to be run from it's directory and cannot be accessed directly
os.chdir("../extparsers/geniatagger-3.0.1")
child = pexpect.spawn("./geniatagger ../../input/testsentences.in" )
child = [i for i in child]
results = [i.decode("utf-8") for i in child[4:]]
print(results)

os.chdir(curdir)