#!/usr/bin/env python

import string
import sys
import shutil
from collections import Counter

cmInInch = 2.54

def toInchString(kicadDrill):
	return format(kicadDrill / 10000.0, ".4f") + '"'

def toMMString(kicadDrill):
	return str(round(kicadDrill * cmInInch / 1000, 1)) + 'mm'

fin = open(sys.argv[1],'r')
fout = open('tmp.brd', 'w')

changesList = []
allDrills = []

for line in fin.readlines(): 
	if line.startswith('Dr '):
		tokens = line.split()

		# Drill sizes are stored in 1/10000'ths of an inch
		microMeterDrill = int(round(float(tokens[1]) * cmInInch, -2))
		inchDrill = int(round(microMeterDrill / cmInInch))

		line = line.replace(tokens[1], str(inchDrill))
		if tokens[1] != str(inchDrill):
			changesList.append((int(tokens[1]), inchDrill))
#			sys.stdout.write(tokens[1] + ' -> ' + str(inchDrill) + '\n')
#		sys.stdout.write(line)
		allDrills.append(inchDrill)
	fout.write(line)

changesCounter = Counter(changesList)
sys.stdout.write('\n')
#sys.stdout.write(str(changesCounter) + '\n')
if len(changesCounter) == 0:
	sys.stdout.write("No drill sizes changed\n")
else:
	sys.stdout.write("Drill changes summary:\n")
	for change in sorted(changesCounter.keys()):
		sys.stdout.write(toInchString(change[0]) + ' --> ' + toInchString(change[1]) + ' ' + toMMString(change[1]) + ' :  ' + str(changesCounter[change]) + 'x\n')

sys.stdout.write("\n")
sys.stdout.write("Drills summary:\n")
drillsCounter = Counter(allDrills)
#sys.stdout.write(str(drillsCounter) + '\n')
for drill in sorted(drillsCounter.keys()):
	sys.stdout.write(toInchString(drill) + ' ' + toMMString(drill) + ' :  ' + str(drillsCounter[drill]) + ' hole(s)\n')

fin.close()
fout.close()

shutil.copy(sys.argv[1], sys.argv[1] + '.backup')
shutil.move('tmp.brd', sys.argv[1])
