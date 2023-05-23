import csv


def read_transitivities(file_path):
    result = {}
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            verb = row[0]
            transitive = row[1] == 'transitive'
            intransitive = row[2] == 'intransitive'
            
            result[verb] = {'transitive': transitive, 'intransitive': intransitive}
    
    return result