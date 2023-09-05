def translate_aa(tree,adpCSV):
    adpRes = []
    found = False
    for row in adpCSV:
        if row[6] == tree['word']:
            adpRes.append((row[0],{'NF':row[5], 'S':row[4]}))
            found = True
    if not found:
        adpRes.append((tree['word'],{'NF':'O', 'S':'S'}))
        adpRes.append((tree['word'],{'NF':'O', 'S':'0'}))
        adpRes.append((tree['word'],{'NF':'0', 'S':'S'}))
        adpRes.append((tree['word'],{'NF':'0', 'S':'0'}))
    return adpRes