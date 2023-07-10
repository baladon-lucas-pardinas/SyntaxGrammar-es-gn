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
            if (row[7] == '0'):
                verb = row[0]
                verbs.append((verb,{'AGR':{}, 'MOOD':row[3],'NEG':'0','POS':row[8]}))
                verb = negate_verb(row)
                verbs.append((verb,{'AGR':{}, 'MOOD':row[3],'NEG':'1','POS':row[8]}))
            else:
                verb = row[0]
                verbs.append((verb,{'AGR':{'INC':row[7]}, 'MOOD':row[3],'NEG':'0','POS':row[8]}))
                verb = negate_verb(row)
                verbs.append((verb,{'AGR':{'INC':row[7]}, 'MOOD':row[3],'NEG':'1','POS':row[8]}))
    return verbs

def negate_verb(row):
    raiz = row[1]
    parts = row[0].split(raiz,1)
    if nasal(raiz):
        neg_inicial = 'n'
    else:
        neg_inicial = 'nd'
    match parts[0]:
        case 'ja':
            neg_inicial += 'a'
        case 're':
            neg_inicial += 'e'
        case 'ro':
            neg_inicial += 'o'
        case 'pe':
            neg_inicial += 'a'
        case 'ña':
            neg_inicial += 'a'
    if raiz[len(raiz) - 1] in ['i', 'í','ĩ']:
        neg_final = 'ri'
    else:
        neg_final = 'i'
    negated = neg_inicial + parts[0] + raiz + neg_final + parts[1]
    return (negated)

def nasal(verb):
    nasal = False
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ','g̃', 'm', 'n', 'ñ', 'mb', 'nd', 'ng', 'nt']
    if any(nas in verb for nas in nasals):
        nasal = True 
    return nasal