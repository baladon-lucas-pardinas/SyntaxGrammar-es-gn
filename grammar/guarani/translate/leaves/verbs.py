def translate_verbs(tree,verbCSV):
    verbs = []
    label = tree['label']
    agreement = label['AGR']
    mood = label['MOOD']
    tense = agreement['TENSE']
    per = agreement['PER']
    num = agreement['NUM']
    found = False

    for row in verbCSV:
        if row[12] == tree['word'] and row[16].lower() == mood.lower() and row[17].lower() == tense.lower() and row[18] == str(per) and row[19].lower() == num.lower():
            verb = row[0] + ' *'
            if (special_verb(row[1])):
                verbs.append((verb,{'AGR':{}, 'MOOD':row[3],'NEG':str(0),'POS':row[8]}))
                if (irregular(row[1])):
                    verb = negate_irregular(row)
                verbs.append((verb,{'AGR':{}, 'MOOD':row[3],'NEG':str(1),'POS':row[8]}))
            else:
                if (row[7] == '0'):
                    verbs.append((verb,{'AGR':{}, 'MOOD':row[3],'NEG':str(0),'POS':row[8]}))
                    verb = negate_verb(row)
                    verbs.append((verb,{'AGR':{}, 'MOOD':row[3],'NEG':str(1),'POS':row[8]}))
                else:
                    verbs.append((verb,{'AGR':{'INC':row[7]}, 'MOOD':row[3],'NEG':str(0),'POS':row[8]}))
                    verb = negate_verb(row)
                    verbs.append((verb,{'AGR':{'INC':row[7]}, 'MOOD':row[3],'NEG':str(1),'POS':row[8]}))
            found = True
    if not found:
        if num == 'P' and per == '2':
            verbs.append((tree['word'],{'AGR':{'INC':'I'}, 'MOOD':mood,'NEG':str(0),'POS':'B'}))
            verbs.append((tree['word'],{'AGR':{'INC':'I'}, 'MOOD':mood,'NEG':str(0),'POS':'P'}))
            verbs.append((tree['word'],{'AGR':{'INC':'E'}, 'MOOD':mood,'NEG':str(0),'POS':'B'}))
            verbs.append((tree['word'],{'AGR':{'INC':'E'}, 'MOOD':mood,'NEG':str(0),'POS':'P'}))
            new_verb = negate_spanish_verb(tree['word'])
            verbs.append((new_verb,{'AGR':{'INC':'I'}, 'MOOD':mood,'NEG':str(1),'POS':'B'}))
            verbs.append((new_verb,{'AGR':{'INC':'I'}, 'MOOD':mood,'NEG':str(1),'POS':'P'}))
            verbs.append((new_verb,{'AGR':{'INC':'E'}, 'MOOD':mood,'NEG':str(1),'POS':'B'}))
            verbs.append((new_verb,{'AGR':{'INC':'E'}, 'MOOD':mood,'NEG':str(1),'POS':'P'}))
        else:
            verbs.append((tree['word'],{'AGR':{}, 'MOOD':mood,'NEG':str(0),'POS':'B'}))
            verbs.append((tree['word'],{'AGR':{}, 'MOOD':mood,'NEG':str(0),'POS':'P'}))
            verbs.append((tree['word'],{'AGR':{}, 'MOOD':mood,'NEG':str(0),'POS':'B'}))
            verbs.append((tree['word'],{'AGR':{}, 'MOOD':mood,'NEG':str(0),'POS':'P'}))
            new_verb = negate_spanish_verb(tree['word'])
            verbs.append((new_verb,{'AGR':{}, 'MOOD':mood,'NEG':str(1),'POS':'B'}))
            verbs.append((new_verb,{'AGR':{}, 'MOOD':mood,'NEG':str(1),'POS':'P'}))
            verbs.append((new_verb,{'AGR':{}, 'MOOD':mood,'NEG':str(1),'POS':'B'}))
            verbs.append((new_verb,{'AGR':{}, 'MOOD':mood,'NEG':str(1),'POS':'P'}))
    return verbs

def negate_spanish_verb(verb):
    return 'no ' + verb

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
    negated = neg_inicial + parts[0] + raiz + neg_final + parts[1] + ' *'
    return (negated)

def negate_irregular(row):
    raiz = row[1]
    verb = row[0]
    spanish_verb_root = row[13]
    neg_final = ''
    neg_inicial = ''
    match raiz:
        case '‘a':
            start = verb[0:4]
            end = verb[4:]
            neg_inicial = 'nde'
            neg_final = 'i'
        case '‘u':
            match spanish_verb_root:
                case 'comer':
                    start = verb[0:4]
                    end = verb[4:]
                    neg_inicial = 'nde'
                    neg_final = 'i'
                case _:
                    start = verb[0:5]
                    end = verb[5:]
                    neg_inicial = 'nde'
                    neg_final = 'i'
        case 'yguy':
            start = verb[0:7]
            end = verb[7:]
            neg_inicial = 'nde'
            neg_final = 'i'
        case 'yta':
            start = verb[0:6]
            end = verb[6:]
            neg_inicial = 'nde'
            neg_final = 'i'
        case '‘e':
            match verb[0:3]:
                case 'ere':
                    start = verb[0:3]
                    end = verb[3:]
                    neg_inicial = 'nd'
                case _:
                    start = verb[0:4]
                    end = verb[4:]
                    neg_inicial = 'nde'
            neg_final = 'i'
        case 'ha':
            match verb[0:3]:
                case 'aha':
                    start = verb[0:3]
                    end = verb[3:]
                    neg_inicial = 'nd'
                case 'oho':
                    start = verb[0:3]
                    end = verb[3:]
                    neg_inicial = 'nd'
                case _:
                    start = verb[0:4]
                    end = verb[4:]
                    neg_inicial = 'nde'
            neg_final = 'i'
    negated = neg_inicial + start + neg_final + end + ' *'
    return negated

def nasal(verb):
    nasal = 'O'
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ','g̃', 'm', 'n', 'ñ', 'mb', 'nd', 'ng', 'nt']
    if any(nas in verb for nas in nasals):
        nasal = 'N' 
    return nasal

def special_verb(verb):
    return irregular(verb) or defective(verb)

def irregular(verb):
    irregulares = ["‘a","‘u","yguy","yta","‘e","ha"]
    return verb in irregulares

def defective(verb):
    defectivos = ["ko'i", "je'ói", "hua'ĩ"]
    return verb in defectivos
