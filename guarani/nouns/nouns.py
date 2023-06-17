import csv
import codecs

def final_nasal(noun):
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ']
    ñs = ['ña', 'ñe', 'ñi', 'ño', 'ñu', 'ñy']
    return (noun[len(noun)-1] in nasals) or (noun[len(noun)-2] in nasals) or (noun[(len(noun)-2):] in ñs)

def es_nasal(noun):
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ', 'ñ', 'm', 'n']
    return any(n in nasals for n in noun)

def no_tonica(noun):
    tonica = ['á','é','í','ó','ú','ý']
    return any(n in tonica for n in noun)

def principio_tonica(noun):
    tonica = ['á','é','í','ó','ú','ý']
    return noun[0] in tonica

def principio_vocal(noun):
    vocal = ['a','e','i','o','u','y']
    return noun[0] in vocal

def final_vocal(noun):
    vocal = ['a','e','i','o','u','y']
    return noun[len(noun)-1] in vocal

def final_tonica(noun):
    tonica = ['á','é','í','ó','ú','ý','ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ']
    return noun[len(noun)-1] in tonica

def comienzo_consonante(noun):
    vocales =['á','é','í','ó','ú','ý','ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ','a','e','i','o','u','y']
    return not noun[0] in vocales

def read_csv(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as file:
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
    with codecs.open(filepath, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def write_nouns(nouns):
    final = []
    for line in nouns:
        especialTercera = 6
        if line[6] == 'P':
            noun = plural(line[0])
            number = 'P'
        else:
            noun = line[0]
            number = line[6]
        if es_nasal(noun):
            nasal = 'N'
        else:
            nasal = 'O'
        if noun[0] in ['n','o']:
            especialTercera = 1
        elif (not es_nasal(noun)) and principio_vocal(noun) and final_tonica(noun):
            print(noun)
            especialTercera = 2
        elif es_nasal(noun) and principio_vocal(noun) and final_tonica(noun):
            especialTercera = 3
        elif comienzo_consonante(noun):
            especialTercera = 4
        elif principio_tonica(noun) and final_vocal(noun):
            especialTercera = 5
        final.append([noun, line[0],'N','C','0',number,especialTercera,nasal]+line[1:])
    return final

def separar_nouns(nouns):
    final = []
    for v in nouns:
        vlist = v[0].split("_")
        #vlist2 = vlist[0].split('\"')
        for i in vlist:
            i = i.replace(",","")
            #j = i.replace('\"','')
            f = [i] + v[1:]
            final.append(f)
    return final


def main():
    nouns = read_csv("matched-nouns.csv")
    nouns = separar_nouns(nouns)
    final = write_nouns(nouns)
    write_to_csv("finished-nouns.csv", final)

main()