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

2) The number of possible sets can be huge (10+ millions), therefore the maximum size of the sets has a default value of 5. The user can increase this value (optional argument) but may need to increase the available memory to avoid an error. 

3) It is assumed that the elements in the rows are sorted. If it is not the case, the option --needs_sorting must be used. Assuming that the rows are sorted instead of verifying it saves time.

### Files ###

readme.md : this file

supermarket_optimization.py : the script

retail_25k.dat : the input file provided for the exercise

output_size-3_freq-4 : the result of the script for input=retail_25k.dat with sets_min_size=3 and support_level=4 (and a maximum size set of 5 (inclusive) to avoid a memory error with the computer it was run from)

test.txt : a small input test file

test_output.txt : the output for the test file

algo.txt : a simplified version of the algorithm present in the code
