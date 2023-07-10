def translate_pronouns(tree,pronounCSV):
    pronounsRes = []
    label = tree['label']
    agreement = label['AGR']
    num = agreement['NUM']
    per = agreement['PER']
    for row in pronounCSV:
        if row[11] == tree['word'] and row[4] == per and row[6].lower() == num.lower():
            if row[9] == '0':
                pronounsRes.append((row[0],{'AGR':{'INC':row[7], 'POS':row[8]}}))
            else:
                pronounsRes.append((row[0],{'AGR':{'INC':row[7], 'POS':row[8], 'NAS':row[9]}}))
    return pronounsRes