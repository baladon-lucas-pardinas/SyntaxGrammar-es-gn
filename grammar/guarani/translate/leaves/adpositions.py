def translate_adpositions(tree,adpCSV):
    adpRes = []
    found = False
    for row in adpCSV:
        if row[6] == tree['word']:
            if (row[5] == '0'):
                adpRes.append((row[0],{'AGR':{}, 'U':row[3], 'S':row[4],'NF':'N'}))
                adpRes.append((row[0],{'AGR':{}, 'U':row[3], 'S':row[4],'NF':'O'}))
            else:
                if (row[3] == 'U'):
                    adpRes.append((row[0],{'AGR':{}, 'U':row[3], 'S':row[4],'NF':row[5]}))
                else:
                    adpRes.append((row[0],{'AGR':{'NAS':row[5]}, 'U':row[3], 'S':row[4],'NF':'N'}))
                    adpRes.append((row[0],{'AGR':{'NAS':row[5]}, 'U':row[3], 'S':row[4],'NF':'O'}))
            found = True
    if not found:
        adpRes.append((tree['word'],{'AGR':{}, 'U':'U', 'S':'S','NF':'O'}))
        adpRes.append((tree['word'],{'AGR':{}, 'U':'U', 'S':'0','NF':'O'}))
        adpRes.append((tree['word'],{'AGR':{}, 'U':'U', 'S':'0','NF':'0'}))
        adpRes.append((tree['word'],{'AGR':{}, 'U':'U', 'S':'S','NF':'0'}))
        adpRes.append((tree['word'],{'AGR':{'NAS':nasal_spanish(tree['word'])}, 'U':'S', 'S':'S','NF':'O'}))
        adpRes.append((tree['word'],{'AGR':{'NAS':nasal_spanish(tree['word'])}, 'U':'S', 'S':'S','NF':'0'}))
        adpRes.append((tree['word'],{'AGR':{'NAS':nasal_spanish(tree['word'])}, 'U':'S', 'S':'0','NF':'O'}))
        adpRes.append((tree['word'],{'AGR':{'NAS':nasal_spanish(tree['word'])}, 'U':'S', 'S':'0','NF':'0'}))
    return adpRes

def nasal_spanish(verb):
    nasal = False
    nasals = ['m', 'n', 'ñ', 'mb', 'nd', 'ng', 'nt']
    if any(nas in verb for nas in nasals):
        nasal = True 
    return nasal