import sys
import os
import getopt

if __name__ == '__main__':

	out_file = '../sounds/hello.wav'
	length = 5
	opts, args = getopt.getopt(sys.argv[1:], 'd:')
	for o, a in opts: 
		if o == '-f':
			out_file = a
		if o == '-l':
			length = a
	os.system('arecord -f S16_LE -c 2 -r 96000 -d ' + str(length) + ' ' + out_file)
