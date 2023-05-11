### Example usage:
### python find-unique.py matched-verbs.csv [unique-output.csv]

import csv
import sys

def read_arguments():
    if len(sys.argv) > 1:
        return sys.argv
    else:
        raise Exception("Not enough arguments were provided")
  
def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix
    
def find_unique(matrix):
    unique = list(dict.fromkeys([x[2] for x in matrix]))
    return unique

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def main():
    args = read_arguments()
    words_file = args[1]
    output_file = None
    if (len(args) > 2):
        output_file = args[2]
    spanish_words = read_csv(words_file)
    unique = find_unique(spanish_words)
    print("Unique words: " + str(len(unique)))
    if output_file:
        write_to_csv(output_file, [[x] for x in unique])


if __name__ == '__main__':
    main()