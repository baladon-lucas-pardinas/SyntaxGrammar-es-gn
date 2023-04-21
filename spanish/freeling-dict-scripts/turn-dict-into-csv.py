### Example usage:
### python turn-dict-into-csv.py ../freeling-espanol

import csv
import os
import sys

def read_arguments():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        raise Exception("Not enough arguments were provided")


def list_files(directory):
    return [os.path.abspath(os.path.join(directory, f)) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def turn_into_csv(filepath):
    outFilePath = filepath + '.csv'
    with open(filepath, 'r') as in_file, open(outFilePath, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        for line in in_file:
            line = line.strip().split()
            row = line[:2]
            for letter in line[2]:
                row.append(letter)
            writer.writerow(row)



def main():
    dicsDirectory = read_arguments()
    files = list_files(dicsDirectory)
    for file in files:
        turn_into_csv(file)
    
if __name__ == '__main__':
    main()