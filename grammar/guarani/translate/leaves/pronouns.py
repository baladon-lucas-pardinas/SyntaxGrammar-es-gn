def translate_pronouns(tree,pronounCSV):
    pronounsRes = []
    label = tree['label']
    agreement = label['AGR']
    num = agreement['NUM']
    per = agreement['PER']
    for row in pronounCSV:
        if row[11] == tree['word'] and str(row[4]) == str(per) and row[6].lower() == num.lower():
            if row[10] == '0':
                pronounsRes.append((row[0],{'AGR':{'INC':row[8]}, 'POS':row[9]}))
            else:
                pronounsRes.append((row[0],{'AGR':{'INC':row[8]}, 'POS':row[9], 'NAS':row[9]}))
    return pronounsRes