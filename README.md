# supermarket-optimization

### General information ###
This script takes as input a series of transactions and provides sets of elements that frequently appear together.

Input : file in which each line contains space-seperated integers

Output : file in which each line contains a set size, its frequency in the input file and all its elements. All the numbers are separated by a comma and a space. Example :
3, 4, 1, 5, 8
a set containing 3 elements {1, 5, 8} that appear together in 4 different rows

### Launch ###
Basic command to execute the script :
python.exe supermarket_optimization.py [input_file_name]

For more information and optional arguments :
python.exe supermarket_optimization.py -h

Example of a command :
python.exe supermarket_optimization.py input.txt -o output.txt --support_level 4 --sets_min_size 5 --needs_sorting

### Notes ###

1) All combinations are taken into accounts, even those that overlap. For example, given the following sets associated with their frequency :
{1, 2, 3} --> 5
{3, 4, 5, 6} --> 4
And given the new line of transactions :
1 2 3 4 5 6
We will obtain :
{1, 2, 3} --> 6
{3, 4, 5, 6} --> 5
Which means that the number "3" is taken into account for two different sets.

2) It is assumed that the elements in the rows are sorted. If it is not the case, the option --needs_sorting must be used. Assuming that the rows are sorted instead of verifying it saves time.

### Files ###

Input files :
retail_25k.dat : the file provided for the exercise
test.txt : a small test file

Output files :
output_size-3_freq-4 : the result of the script for input=retail_25k.dat with sets_min_size=3 and support_level=4 (and a maximum size set of 5 (inclusive) to avoid a memory error with the computer it was run from)
test_output.txt : the output for the test file

### General algorithm ###

This is a simplified version of the algorithm present in the code.

(1) Go through the transactions :
	relevant_rows = []
	max_set_size = 0
  element_to_occurrences = {}
  for each line :
		if line contains less elements than the min_size :
			ignore it
		else :
			relevant_rows.add(line)
			if number of elements n in line > max_set_size :
				max_set_size = n
			for each element in line :
				element_to_occurrences.update(element)
					
(2) Go through the elements :
	// to save time and space, each element is entirely processed and then removed from all the rows before the next element is processed
  // to save space :
  // - less frequent elements are processed first, so that the greedier elements are processed at the end, when the rows are much lighter
  // - each set size is processed entirely (with the result written in the output file) so that the main data structure can be emptied before processing the next set size
  element_to_occurrences.sort(sortBy=occurrences)
	open the output file f in writing
	create a map m that maps sets of elements to their frequencies
	for each element e :
		for each set size s (minimum : 3, maximum determined in (1)):
			for each row :
				delete from the row the previous element processed
				sets = all sets of size s containing element e
					for each set in sets :
						map.update(set)
			write in output f : 
				for each set in m :
					write : <set.size()>, <map.getValue(set)>, <set[0]>, <set[1]>, etc.
			m = {} // empty the map
		previous_element = element
