def translate_pronouns(tree,pronounCSV):
    pronounsRes = []
    label = tree['label']
    agreement = label['AGR']
    num = agreement['NUM']
    per = agreement['PER']
    found = False

    for row in pronounCSV:
        if row[11] == tree['word'] and str(row[4]) == str(per) and row[6].lower() == num.lower():
            pronounsRes.append((row[0],{'AGR':{'INC':row[8]}, 'POS':row[9]}))
            found = True
    if not found:
        pronounsRes.append((tree['word'],{'AGR':{}, 'POS':'B'}))
    return pronounsRes