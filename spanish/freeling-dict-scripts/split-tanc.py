### Example usage:
### python split-tanc.py ../freeling-espanol/MM.tanc.csv

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
    

def create_dict(name):
    return {
        "name" : name,
        "words" : []
    }

def split_tancs(spanish_tancs):
    splits = {}

    categories = [
        ("S", "adpositions"),
        ("C", "conjunctions"),
        ("P", "pronouns"),
        ("D", "determiners"),
        ("I", "interjections"),
        ("F", "punctuations"),
        ("A", "adjectives")
    ]
    for cat in categories:
        splits[cat[0]] = create_dict(cat[1])

    for word in spanish_tancs:
        splits[word[2]]["words"].append(word)

    return splits

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def main():
    tancs_file = read_arguments()
    spanish_tancs = read_csv(tancs_file)
    splits = split_tancs(spanish_tancs)
    for key in splits:
        write_to_csv(splits[key]["name"] + ".csv", splits[key]["words"])
    #print(splits)
 

if __name__ == '__main__':
    main()