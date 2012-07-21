#!/usr/bin/env python

import re
import string
import sys
import shutil

moduledef_pat = re.compile(r'^\$MODULE (.*)$')     # Start of module definition

fin = open(sys.argv[1],'r')
fout = open('tmp.mod', 'w')

module = None		# Current module name (string)
moduleDefs = {}		# module name (string) -> module definition (concatenated string)

for line in fin.readlines(): 
        # Get rid of CR characters (0x0D) and leading/trailing blanks
        stripped = string.replace(line, '\x0D', '').strip()

	# Check for start of module. Get the module name
	match = moduledef_pat.match(stripped)
	if match:
		module = match.group(1)
		moduleDefs[module] = line

	# Check for end-of-module. Unset module name, store the line itself
	elif line.startswith('$EndMODULE'): 
		moduleDefs[module] += line
		module = None

	# Check for end-of-library. Sort and write all modules
        elif line.startswith('$EndLIBRARY'):  
		for name in sorted(moduleDefs.keys()):
			sys.stdout.write("Module: '" + name + "'\n")
			fout.write(moduleDefs[name])
		fout.write(line)

	# Inside a module definition? Append to the definition string
	elif module:
		moduleDefs[module] += line

	# Header lines
	else:
		fout.write(line)

fin.close()
fout.close()

shutil.copy(sys.argv[1], sys.argv[1] + '.backup')
shutil.move('tmp.mod', sys.argv[1]) 
