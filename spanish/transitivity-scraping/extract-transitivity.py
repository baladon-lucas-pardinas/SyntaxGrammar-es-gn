### Example usage:
### python extract-transitivity.py definitions-rae.csv

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
    
def extract_transitivity(matrix):
    for row in matrix:
        definition = row[1]
        row.pop(1)
        if "tr." in definition:
            row.append("transitive")
        else:
            row.append("0")
        if "intr." in definition:
            row.append("intransitive")
        else:
            row.append("0")
    return matrix

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def main():
    definitions_file = read_arguments()
    definitions = read_csv(definitions_file)
    transitivities = extract_transitivity(definitions)
    write_to_csv("output.csv", transitivities)


if __name__ == '__main__':
    main()