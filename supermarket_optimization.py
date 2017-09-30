#!/usr/bin/python
# --*-- coding:utf-8 --*--

'''
author : Audrey Champeau
'''

import argparse

parser = argparse.ArgumentParser(description="Provides frequent sets of elements based on a list of transactions.")
parser.add_argument('input_file', type=str,
                   help='the name of the input file')
parser.add_argument('-o', '--output_file', dest='output_file_name', type=str,
                   help='the name of the output file')
parser.add_argument('-l', '--sets_min_size', dest='sets_min_size', type=int, default=3,
                   help='the minimum size for the sets')
parser.add_argument('-s', '--support_level', dest='support_level', type=int, default=4,
                   help='the support level')
parser.add_argument('-b', '--needs_sorting', dest='needs_sorting', type=bool, default=False,
                   help='the support level')

args = parser.parse_args()

# retrieve arguments to initialize global variables
input_file_name = args.input_file
min_set_size = args.sets_min_size
min_frequency = args.support_level
needs_to_be_sorted = args.needs_sorting

output_file_name = "output_size-"+str(min_set_size)+"_freq-"+str(min_frequency)
if args.output_file_name != None:
	output_file_name = args.output_file_name
out = open(output_file_name, "w") # create the file, strings will be appended afterwards
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
def get_combinations(r, i, s, start=0):
	combinations = []
	r_size = len(r)
	# base cases : 
	# - if the size of the row is smaller than the set size, no set can be found, return an empty list
	# - if the starting point is at the end of the row, all sets have been found, return them
	if (r_size < s or start == r_size-1):
		return combinations
	# recursion
	else:
		# if the starting point is at the element e, go to the next index
		if (start == i):
			return get_combinations(r, i, s, start+1)
		else:
			# find all possible sets in the row that contain the element e 
			elements = r
			comb = []
			# start by putting the element e in the set
			comb.append(r[i])
			r_index = start
			# then fill it with other elements, starting by index start
			while (len(comb) < s):
				if r_index == i:
					r_index += 1
				if r_index >= len(r):
					r_index = 0
				comb.append(r[r_index])
				r_index += 1
			combinations.append(tuple(comb)) # since the rows are sorted, two tuples containing the same elements will always be ordered the same way
			# repeat the operation after incrementing the starting point
			combinations.extend(get_combinations(r, i, s, start+1))
			return combinations

# get a dictionary that associates sets of elements containing a specific element to their frequency	
def get_sets_to_frequency(rows, element, element_to_delete):
	sets_to_frequency = {}
	for row in rows:
		# delete the previous element that has already been processed (all the sets containing the element have already been processed, so the element can be removed from all the rows to save time)
		if element_to_delete != None and element_to_delete in row:
			row.remove(element_to_delete)
		for set_size in range(min_set_size, max_set_size+1):
			if element in row:
				i = row.index(element)
				combinations = get_combinations(row, i, set_size)
				for combination in combinations:
					if combination not in sets_to_frequency:
						sets_to_frequency[combination] = 0
					sets_to_frequency[combination] += 1
	return sets_to_frequency
	
# get the sets that have at least the minimum frequency	
def get_relevant_sets(dic):
	return dict((k, v) for k, v in dic.items() if v >= min_frequency)
	
# write in the output file	
def write_output(file_name, sets_to_frequency):
	with open(file_name, "a") as file:
		for s, f in sets_to_frequency.items():
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
counter = 0
element_to_delete = None
# Process elements one by one (instead of having a very big data structure in memory)
for i, element in enumerate(all_unique_elements):
	counter += 1
	print(str(counter)+"/"+str(total))
	sets_to_frequency = get_sets_to_frequency(relevant_rows, element, element_to_delete)
	relevant_sets_to_frequency = get_relevant_sets(sets_to_frequency)
	write_output(output_file_name, relevant_sets_to_frequency)
	# store the value of the element already processed so that it will be ignored in the next loop
	element_to_delete = element

print ("All done.\nRetrieve results in the file '"+output_file_name+"'.")


