### Example usage:
### python count-unique.py matched-verbs.csv

import csv
import sys

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
    
def count_unique(matrix):
    unique = set([x[2] for x in matrix])
    return len(unique)

def main():
    words_file = read_arguments()
    spanish_words = read_csv(words_file)
    unique = count_unique(spanish_words)
    print("Unique words: " + str(unique))


if __name__ == '__main__':
    main()