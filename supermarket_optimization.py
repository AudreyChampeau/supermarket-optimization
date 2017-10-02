#!/usr/bin/python
# --*-- coding:utf-8 --*--

'''
author : Audrey Champeau

This script provides frequent sets of elements based on a list of transactions.
'''

import argparse
import itertools
import operator

parser = argparse.ArgumentParser(description="Provides frequent sets of elements based on a list of transactions.")
parser.add_argument('input_file', type=str,
                   help='the name of the input file that contains a list of space-separated numbers in each line')
parser.add_argument('-o', '--output_file', dest='output_file_name', type=str,
                   help='the name of the output file')
parser.add_argument('--sets_min_size', dest='sets_min_size', type=int, default=3,
                   help='the minimum size for the sets')
parser.add_argument('--support_level', dest='support_level', type=int, default=4,
                   help='the support level (or frequency)')
parser.add_argument('--needs_sorting', action='store_true',
                   help='if the transactions need to be sorted')

args = parser.parse_args()

# retrieve arguments to initialize global variables
input_file_name = args.input_file
min_set_size = args.sets_min_size
min_frequency = args.support_level
needs_to_be_sorted = args.needs_sorting

output_file_name = "output_size-"+str(min_set_size)+"_freq-"+str(min_frequency)
if args.output_file_name != None:
	output_file_name = args.output_file_name
out = open(output_file_name, "w") # create the file, strings will be appended to it afterwards
out.close()

max_set_size = 0
all_unique_elements = {}
		
# retrieve rows
def retrieve_relevant_rows_from_file(file_name):
	relevant_rows = []
	with open(file_name, "r") as file:
		for line in file:
			split_row = line.strip().split()
			# update the maximum size of the sets (which is equal to the maximum number of elements for one row)
			global max_set_size
			if (len(split_row) > max_set_size):
				max_set_size = len(split_row)
			row = []
			# convert elements of the row from strings to ints
			split_row = list(int(v) for v in split_row)
			# sort the elements
			if (needs_to_be_sorted):
				split_row.sort()
			# remove doubles
			for i in range(len(split_row)):
				r = split_row[i]
				if i == 0 or r != split_row[i-1]:
					row.append(r)
					global all_unique_elements
					if r not in all_unique_elements:
						all_unique_elements[r] = 0
					all_unique_elements[r] += 1
			# if the line contains fewer elements than the minimum set size, no valid set can be taken from it, so the line can be safely ignored
			if (len(row) >= min_set_size):
				relevant_rows.append(row)
	return relevant_rows
	
# get all combinations of size s containing element e of index i in row r
def get_combinations(r, i, s):
	combinations = []
	r_size = len(r)  
	# start by putting aside the element e
	element = []
	element.append(r[i])
	# then get all possible (unordered) combinations of size s-1 of the rest of the elements
	tmp_row = list(r)
	tmp_row.remove(r[i])
	combs = itertools.combinations(tmp_row, s-1)
	# finally, combine them to get all possible combinations of size s that contain element e
	for c in combs:
		set = []
		set.append(r[i])
		for e in c:
			set.append(e)
		combinations.append(tuple(set))
	return combinations

# convert a tuple into a string
def get_string(tuple):
	s = ""
	for t in tuple:
		s += str(t)+"#"
	return s[:len(s)-1]
	
# get a dictionary that associates sets of elements containing a specific element with their frequency
def get_sets_to_frequency(rows, element, set_size, previous_element):
	sets_to_frequency = {}
	for row in rows:
		# an element that has been entirely processed can be safely removed, all sets containing it have already been found
		if previous_element in row:
			row.remove(previous_element)
		if element in row:
			i = row.index(element)
			combinations = get_combinations(row, i, set_size)
			# as the rows are sorted, sets that contain the same elements will always be ordered the same way
			for combination in combinations:
				c = get_string(combination)
				if c not in sets_to_frequency:
					sets_to_frequency[c] = 0
				sets_to_frequency[c] += 1
	return sets_to_frequency
	
# get the sets that have at least the minimum frequency	
def get_relevant_sets(dic):
	return dict((k, v) for k, v in dic.items() if v >= min_frequency)
	
# write in the output file	
def write_output(file_name, sets_to_frequency):
	with open(file_name, "a") as file:
		for k, f in sets_to_frequency.items():
			s = tuple(list(int(v) for v in k.split("#")))
			to_print = str(len(s))+", "+str(f)+", "
			for e in s:
				to_print += str(e)+", "
			file.write(to_print[:len(to_print)-2]+"\n")
	
### MAIN

print ("Start...")

print ("Retrieving and pre-processing data...")
relevant_rows = retrieve_relevant_rows_from_file(input_file_name)

print ("Processing...")
total = len(all_unique_elements)

# sort all elements by ascending occurrences so that rare elements are processed first and frequent elements are processed in the end, when the rows contain fewer elements
sorted_aue = sorted(all_unique_elements.items(), key=operator.itemgetter(1), reverse=True)
all_unique_elements = []
counter = 0
previous_element = None
# Process elements one by one (to avoid having a very big data structure in memory)
for (element, occ) in sorted_aue:
	counter += 1
	print(str(counter)+"/"+str(total)+" [element="+str(element)+" : occurrences="+str(occ)+"]")
	# Process entirely each size at a time (again, to avoid having a very big data structure in memory)
	for set_size in range(min_set_size, max_set_size+1):
		print("set size : "+str(set_size))
		sets_to_frequency = get_sets_to_frequency(relevant_rows, element, set_size, previous_element)
		print("set_to_frequency size : "+str(len(sets_to_frequency)))
		relevant_sets_to_frequency = get_relevant_sets(sets_to_frequency)
		write_output(output_file_name, relevant_sets_to_frequency)
	# store the element that has been processed so that it can be removed of all the rows in the next loop (saving time)
	previous_element = element

print ("All done.\nRetrieve results in the file '"+output_file_name+"'.")


