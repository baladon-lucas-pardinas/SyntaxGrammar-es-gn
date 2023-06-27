import csv


def read_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix