###############################################
#
# Does not work in place. You should point to a different file for output.
# Otherwise the original file will be deleted.
#
###############################################

import csv
import sys

def read_arguments():
    if len(sys.argv) > 2:
        return sys.argv[1], sys.argv[2]
    else:
        raise Exception("Not enough arguments were provided")

def insertion_sort(lst):
    for i in range(1, len(lst)):
        j = i
        while j > 0 and lst[j-1][0] > lst[j][0]:
            lst[j-1], lst[j] = lst[j], lst[j-1]
            j -= 1

def sort_csv_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, \
         open(output_file_path, 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        data = list(reader)
        insertion_sort(data)
        writer = csv.writer(output_file)
        writer.writerows(data)

if __name__ == '__main__':
    [input_file_path, output_file_path] = read_arguments()
    if (input_file_path == output_file_path):
        raise Exception("Input and output file paths should be different")
    sort_csv_file(input_file_path, output_file_path)
