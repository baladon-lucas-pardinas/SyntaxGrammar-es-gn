import csv


def read_transitivities(file_path):
    result = {}
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            verb = row[0]
            transitive = row[1] == 'tr'
            ditransitive = row[2] == 'di'
            intransitive = row[3] == 'intr'
            
            result[verb] = {'transitive': transitive, 'intransitive': intransitive, 'ditransitive' : ditransitive}
    
    return result