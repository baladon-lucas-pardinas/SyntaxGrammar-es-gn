def translate_nouns(tree,nounCSV):
    nounsRes = []
    label = tree['label']
    agreement = label['AGR']
    gen = agreement['GEN']
    num = agreement['NUM']
    for row in nounCSV:
        if row[8] == tree['word'] and row[12].lower() == gen.lower() and row[13].lower() == num.lower():
            nounsRes.append({'noun':row[0], 'tercera':row[6], 'nasal':row[7]})
    return nounsRes