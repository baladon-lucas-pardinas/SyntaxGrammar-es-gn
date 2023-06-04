import os
import xml.etree.ElementTree as ET
import csv

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def merge(ancora,ours):
    res = []
    i = 0
    j = 0
    while (i < len(ours)) & (j < len(ancora)):
        if ancora[j][0] == ours[i][0]:
            res.append(ancora[j])
            i += 1
            j += 1
        elif ours[i][0] > ancora[j][0]:
            j += 1
        elif ours[i][0] < ancora[j][0]:
            tr = '0'
            if ours[i][1] == 'transitive':
                tr = 'tr'
            intr = '0'
            if ours[i][1] == 'intransitive':
                intr = 'intr'
            res.append([ours[i][0],tr,intr,'0'])
            i += 1
    while (i < len(ours)):
        tr = '0'
        if ours[i][1] == 'transitive':
            tr = 'tr'
        intr = '0'
        if ours[i][1] == 'intransitive':
            intr = 'intr'
        res.append([ours[i][0],tr,intr,'0'])
        i += 1
    return res

def fullmerge(transitives,all):
    res = []
    i = 0
    j = 0
    while j < len(all) and i < len(transitives):
        if transitives[i][0] == all[j][2]:
            res.append(all[j]+transitives[i][1:])
        elif transitives[i+1][0] == all[j][2]:
            i += 1
            res.append(all[j]+transitives[i][1:])
        else:
            print('ERROR ' + transitives[i][0] + ' ' + all[j][2])
        j += 1
    return res


def main():
    ancora = read_csv("./final-transitivity.csv")
    ours = read_csv("../spanish/transitivity-scraping/transitivities.csv")
    merged = merge(ancora,ours)
    write_to_csv("merged-transitivities.csv", merged)
    oursfull = read_csv("../spanish/spanish-verbs/matched-verbs.csv")
    allmerged = fullmerge(merged,oursfull)
    write_to_csv("fullymerged-transitivities.csv", allmerged)

main()