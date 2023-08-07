def translate_adpositions(tree,adpCSV):
    adpRes = []
    for row in adpCSV:
        if row[6] == tree['word']:
            if (row[5] == '0'):
                adpRes.append((row[0],{'AGR':{}, 'S':row[4]}))
            else:
                if (row[3] == 'U'):
                    adpRes.append((row[0],{'AGR':{}, 'U':row[3], 'S':row[4],'NF':row[5]}))
                else:
                    adpRes.append((row[0],{'AGR':{'NAS':row[5]}, 'U':row[3], 'S':row[4]}))
    return adpRes