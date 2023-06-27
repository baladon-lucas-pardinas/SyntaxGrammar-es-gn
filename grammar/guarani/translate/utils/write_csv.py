import csv
import codecs

def write_to_csv(filepath, rows):
    with codecs.open(filepath, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)