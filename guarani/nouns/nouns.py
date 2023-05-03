import csv

def final_nasal(noun):
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ']
    ñs = ['ña', 'ñe', 'ñi', 'ño', 'ñu', 'ñy']
    return (noun[len(noun)-1] in nasals) or (noun[len(noun)-2] in nasals) or (noun[(len(noun)-2):] in ñs)

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix

def plural(noun):
    nasal = final_nasal(noun)
    if nasal:
        noun = noun + 'nguéra'
    else: 
        noun = noun + 'kuéra'
    return noun

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def write_nouns(nouns):
    final = []
    for line in nouns:
        if line[6] == 'P':
            noun = plural(line[0])
            number = 'P'
        else:
            noun = line[0]
            number = 'S'
        final.append([noun, line[0],'N','C','0',number]+line[1:])
    return final


def main():
    nouns = read_csv("matched-nouns.csv")
    final = write_nouns(nouns)
    write_to_csv("finished-nouns.csv", final)

main()