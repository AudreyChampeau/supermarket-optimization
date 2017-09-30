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
python.exe supermarket_optimization.py input.txt -o output.txt -l 4 -s 5 -b 1

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

2) It is assumed that the elements in the rows are sorted. If it is not the case, the option --needs_sorting (or -b) must be used. Assuming that the rows are sorted instead of verifying it saves time.

### Files ###

Input files :
retail_25k.dat : the file provided for the exercise
test.txt : a small test file

Output files :
output_size-3_freq-4 : the result of the script for input=retail_25k.dat with size=3 and support_level=4 
