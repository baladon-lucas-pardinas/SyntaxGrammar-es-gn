def translate_aa(tree,adpCSV):
    adpRes = []
    for row in adpCSV:
        if row[6] == tree['word']:
            adpRes.append((row[0],{'NF':row[5], 'S':row[4]}))
    return adpRes