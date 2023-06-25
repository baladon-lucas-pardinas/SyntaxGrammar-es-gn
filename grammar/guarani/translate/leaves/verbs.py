def translate_verbs(tree,verbCSV):
    verbs = []
    label = tree['label']
    agreement = label['AGR']
    mood = label['MOOD']
    tense = agreement['TENSE']
    per = agreement['PER']
    num = agreement['NUM']
    for row in verbCSV:
        if row[12] == tree['word'] and row[16].lower() == mood.lower() and row[17].lower() == tense.lower() and row[18] == str(per) and row[19].lower() == num.lower():
            verbs.append((row[0],{'INC':row[7],'POS':row[8]}))
    return verbs