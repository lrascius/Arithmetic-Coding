import numpy
import math
import string
from bigfloat import *

def encode(string, N):
	# define the precision
	with precision(10000):
		# get the alphabet a-z
		alphabet = list(map(chr, range(97, 123)))
		# get the probability table and initilize it to a uniform distribution of 1
		pdftable = dict((letter, alphabet.count(letter)) for letter in set(alphabet))
		cdfarray = numpy.cumsum(list(pdftable.values()))
		# get the cdftable 
		cdftable = dict(zip(alphabet, cdfarray))

		# initialize the low and high range 
		low = BigFloat.exact('0.0', precision=10000)
		high = BigFloat.exact('1.0', precision=10000)
		# inlitialize the current_range to 0
		current_range = BigFloat.exact('0.0', precision=10000)
		# initilize the low range of symbol to 0
		low_range_of_symbol = BigFloat.exact('0.0', precision=10000)
		# initilize the high range of symbol to 0
		high_range_of_symbol = BigFloat.exact('0.0', precision=10000)

		symbol = ""

		for i in range(0, int(len(string)), N):
			# get the last part to loop when n doesnt divide len(string) evenly, the last part will be len(string) mod n
			if (i+N) > len(string):
				last = len(string) - i
			# else we continue looping n symbols at a time	
			else:
				last = N
			for j in range(i, i + last):
				symbol = string[j]
				# Get the low range of symbol
				if symbol == 'a':
					low_range_of_symbol = 0
				else:
					low_range_of_symbol = (float(cdftable[alphabet[alphabet.index(symbol) - 1]]) / cdftable[alphabet[-1]])	
				# Get the high range of symbol
				high_range_of_symbol = (float(cdftable[symbol]) / cdftable[alphabet[-1]])

				# compute the range 
				current_range = high - low
				# compute the new high
				high = low + current_range * high_range_of_symbol
				# conpute the new low
				low = low + current_range  * low_range_of_symbol

				# once we have our range we update the symbol table
				pdftable[string[j]]+=1
				cdfarray = numpy.cumsum(list((coordinate[1]) for coordinate in sorted(pdftable.items())))
				cdftable = dict(zip(alphabet, cdfarray))

		return low, len(string)