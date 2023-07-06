def translate_nouns(tree,nounCSV):
    nounsRes = []
    label = tree['label']
    agreement = label['AGR']
    gen = agreement['GEN']
    num = agreement['NUM']
    for row in nounCSV:
        if row[8] == tree['word'] and row[12].lower() == gen.lower() and row[13].lower() == num.lower():
            nounsRes.append((row[0],{'AGR':{'NAS':row[7]}, 'NW':final_nasal(row[0]), 'TER':row[6]}))
    return nounsRes

def final_nasal(noun):
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ']
    ñs = ['ña', 'ñe', 'ñi', 'ño', 'ñu', 'ñy']
    if (noun[len(noun)-1] in nasals) or (noun[len(noun)-2] in nasals) or (noun[(len(noun)-2):] in ñs):
        return 'N'
    else:
        return 'O'