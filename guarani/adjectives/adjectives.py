import csv

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix
    
def write_to_csv(filepath, rows):
    with open(filepath, 'w',newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def main():
    adj = read_csv("matched-adjectives.csv")
    matched = []
    for a in adj:
        line = [a[0],a[0],'A','Q'] + a[2:]
        matched.append(line)
    write_to_csv("matched-adjectives-guarani.csv", matched)

main()