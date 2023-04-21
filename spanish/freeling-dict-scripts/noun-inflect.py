### Example usage:
### python noun-inflect.py bilingual-dict.txt ../MM.nom.csv

import csv
import sys

def read_arguments():
    if len(sys.argv) > 2:
        return sys.argv[1], sys.argv[2]
    else:
        raise Exception("Not enough arguments were provided")


def read_dict(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        matrix = []
        for line in lines:
            words = line.strip().split(' ')
            cat, gn, es = words[0], words[1].split(':')[1], words[2].split(':')[1]
            matrix.append([cat, gn, es])
        return matrix
    
def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix
    
def match_nouns(bilingual, spanish_nouns):
    matched = []
    unmatched = []
    for bi_row in bilingual:
        found = False
        if bi_row[0] == 'n':
            for noun_row in spanish_nouns:
                if noun_row[1] == bi_row[2] or noun_row[0] == bi_row[2]:
                    matched.append([bi_row[1]] + noun_row[:-3])
                    found = True
            if not found:
                unmatched.append(bi_row)
    return (matched, unmatched)

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def main():
    dict_file, nouns_file = read_arguments()
    bilingual = read_dict(dict_file)
    spanish_nouns = read_csv(nouns_file)
    (matched_nouns, unmatched_nouns) = match_nouns(bilingual, spanish_nouns)
    write_to_csv("matched-nouns.csv", matched_nouns)
    write_to_csv("unmatched-nouns.csv", unmatched_nouns)


if __name__ == '__main__':
    main()