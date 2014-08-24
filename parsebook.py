#!/opt/local/bin/python
#

import sys
import os
import re
from os.path import basename

MAX_CHARS = 144
NEWLINE="\n"
ELLIPSIS="[...]"

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "input file expected"
		sys.exit(1)
	fname = sys.argv[1]
	parts = os.path.splitext(fname)
	fname_out = parts[0] + ".out" + parts[1]
	f = open( fname,"r")
	fo = open( fname_out , "w" )
	if f is None:
		print "Could not open input file"
		sys.exit(1)
	line = f.readline()
	linecount = 0
	buff = ""
	while len(line) > 0 or len(buff) > 0:
		ended = len(line) == 0
		line = " ".join( re.split(r'[\n\r\t]+',line) )
		line = line.strip()
		print "< "+line
		if len( line ) >= 1 or ended:
			if len( buff ) > 0:
				mount = buff
				if buff[ -1 ] != ' ':
					mount += " "
				line = mount + line
				buff = ""
			if len(line) < MAX_CHARS and not ended:
				print "...%d" % len(line)
				buff = line
			else:
				pattern = re.compile(r'.*?[;!\.\?]+["\',]*')
				aggregator = ""
				counter = 0
				saver = None
				c = -1
				pos = 0
				match = pattern.search(line,pos)
				hanging = None
				while match:
					x = line[match.start():match.end()]
					if hanging != None:
						x = hanging + x
						hanging = None
					pos = match.end()
					skip = False
					if re.match(r'.* [A-Z][a-z]{1,2}\.$', x):
						hanging = x
						skip = True
					if not skip:
						c += 1
						candidate = None
						if saver != None:
							candidate = saver + x
						elif len( x ) < 3:
							saver = x
						else:
							candidate = x
						if candidate != None:
							if counter + len( candidate ) > MAX_CHARS:
								break
							else:
								counter += len(candidate)
								aggregator += candidate 
					match = pattern.search(line,pos)
				if counter <= len(line) and not ended:
					buff = line[counter:len(line)]
				else:
					buff = ""
				if len( aggregator ) == 0 and counter == 0:
					aggregator = line
					buff = ""
					while len(aggregator) + len(ELLIPSIS) > MAX_CHARS:
						lastword = re.search(r'[ ]+',aggregator[::-1])
						if lastword != None:
							keeper = aggregator
							mpoint = len(aggregator) - lastword.end()
							aggregator = aggregator[0:mpoint ]
							buff = keeper[mpoint   : len(keeper)] + buff
					aggregator = aggregator.strip() + ELLIPSIS
				aggregator = aggregator.strip()
				if len(aggregator) > MAX_CHARS:
					print "ERROR:"
					print aggregator
					sys.exit(1)
				fo.write(aggregator+NEWLINE)
				print "> " + aggregator
		if len(buff) >= MAX_CHARS:
			line = buff
			buff = ""
		else:
			line = f.readline()
			linecount += 1
	fo.close()
	f.close()
