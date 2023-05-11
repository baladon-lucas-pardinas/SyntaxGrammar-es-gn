### Example usage:
### python merge-results.py output.csv

import csv
import sys

FILENAME_BASE = "run_results_"
AMOUNT_OF_FILES = 9

def read_arguments():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Not enough arguments were provided")
  
def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix
    
def merge_files(files_amount, filename_base):
    output = []
    for i in range(1, files_amount+1):
         run_result = read_csv(filename_base + str(i) + ".csv")
         run_result = run_result[1:-1] # Remove header and footer
         output = output + run_result
    return output

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def main():
    output_file = read_arguments()
    output = merge_files(AMOUNT_OF_FILES, FILENAME_BASE)
    write_to_csv(output_file, output)


if __name__ == '__main__':
    main()