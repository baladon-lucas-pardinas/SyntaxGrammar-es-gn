def translate_nouns(tree,nounCSV):
    nounsRes = []
    label = tree['label']
    agreement = label['AGR']
    gen = agreement.get('GEN') if agreement.get('GEN') else 'C'
    num = agreement.get('NUM') if agreement.get('NUM') else 'N'
    found = False

    for row in nounCSV:
        if row[8] == tree['word'] and row[12].lower() == gen.lower() and row[13].lower() == num.lower():
            nounsRes.append((row[0],{'AGR':{'NAS':row[7], 'TER':row[6]}, 'NF':final_nasal(row[0])}))
            found = True
    if not found:
        nounsRes.append((tree['word'],{'AGR':{'NAS':nasal_spanish(tree['word'])}, 'NF':'O'}))
    return nounsRes

def final_nasal(noun):
    nasals = ['ã', 'ẽ', 'ĩ', 'õ', 'ũ', 'ỹ']
    ñs = ['ña', 'ñe', 'ñi', 'ño', 'ñu', 'ñy']
    if (noun[len(noun)-1] in nasals) or (noun[len(noun)-2] in nasals) or (noun[(len(noun)-2):] in ñs):
        return 'N'
    else:
        return 'O'
    
def nasal_spanish(verb):
    nasal = 'O'
    nasals = ['m', 'n', 'ñ', 'mb', 'nd', 'ng', 'nt']
    if any(nas in verb for nas in nasals):
        nasal = 'N' 
    return nasal