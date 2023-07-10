def translate_adpositions(tree,adpCSV):
    adpRes = []
    for row in adpCSV:
        if row[6] == tree['word']:
            if (row[5] == '0'):
                adpRes.append((row[0],{'AGR':{}, 'S':row[4]}))
            else:
                adpRes.append((row[0],{'AGR':{'NAS':row[5]}, 'S':row[4]}))
    return adpRes