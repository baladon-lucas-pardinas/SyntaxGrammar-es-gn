### Example usage:
### python adjective-inflect.py dicc_custom.txt all.adjectives.csv

import csv
import sys
import bisect

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
    

def insertion_sort(matrix):
    result = matrix.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j][1] > key[1]:
            result[j+1] = result[j]
            j -= 1
        result[j+1] = key
    return result


def match_adjectives(bilingual, spanish_adjectives):
    matched = []
    unmatched = []
    
    num_matches = num_nonmatches = 0

    # filter bilingual rows and sort them
    sorted_bilingual = sorted([row for row in bilingual if row[0] == 'r'], key=lambda x: x[2])
    print("Total bilingual adjective rows: " + str(len(sorted_bilingual)))

    # sort the adjectives by their base form
    sorted_base = insertion_sort(spanish_adjectives)
    just_bases = [x[1] for x in sorted_base]

    # iterate over filtered bilingual rows and look for matches in sorted Spanish base forms
    for bi_row in sorted_bilingual:
        found = False
        i = bisect.bisect_left(just_bases, bi_row[2])
        while i < len(sorted_base) and sorted_base[i][1] == bi_row[2]:
            matched.append([bi_row[1]] + sorted_base[i])
            i += 1
            found = True
        if (not found):
            unmatched.append(bi_row)
            num_nonmatches += 1
        else:
            num_matches += 1

    print("Matched bilingual rows: " + str(num_matches))
    print("Unmatched bilingual rows: " + str(num_nonmatches))
    
    return (matched, unmatched)

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def main():
    dict_file, adjectives_file = read_arguments()
    bilingual = read_dict(dict_file)
    spanish_adjectives = read_csv(adjectives_file)
    (matched_adjectives, unmatched_adjectives) = match_adjectives(bilingual, spanish_adjectives)
    write_to_csv("matched-adjectives.csv", matched_adjectives)
    write_to_csv("unmatched-adjectives.csv", unmatched_adjectives)


if __name__ == '__main__':
    main()