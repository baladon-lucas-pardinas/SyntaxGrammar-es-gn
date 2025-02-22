def translate_determiners(tree,detCSV):
    dets = []
    label = tree['label']
    agreement = label['AGR']
    gen = agreement.get('GEN') if agreement.get('GEN') else 'C'
    num = agreement.get('NUM') if agreement.get('NUM') else 'N'
    typ = label['TYPE']
    possPer = label['POSSPER']
    possNum = label['POSSNUM']
    found = False

    ## Tener cuidado de solo mirar TER cuando se conjuga en tercera persona
    ## Actualmente la presencia (PRES) no se utiliza
    for row in detCSV:
        if row[12] == tree['word'] and row[15].lower() == typ.lower() and row[18].lower() == num.lower() and row[17].lower() == gen.lower() and row[16] == str(possPer) and row[19].lower() == str(possNum).lower():
            if row[9] != '0':
                if (row[4] == '3'):
                    dets.append((row[0],{'AGR':{'PER':row[4],'NUM':row[6],'POSS':row[7],'INC': row[8], 'NAS':row[9], 'TER':row[10],'PRES':row[11]}}))
                else:
                    dets.append((row[0],{'AGR':{'PER':row[4],'NUM':row[6],'POSS':row[7],'INC': row[8], 'NAS':row[9],'PRES':row[11]}}))
            else:
                if (row[4] == '3'):
                    dets.append((row[0],{'AGR':{'PER':row[4],'NUM':row[6],'POSS':row[7],'INC': row[8], 'NAS':'N', 'TER':row[10],'PRES':row[11]}}))
                    dets.append((row[0],{'AGR':{'PER':row[4],'NUM':row[6],'POSS':row[7],'INC': row[8], 'NAS':'O', 'TER':row[10],'PRES':row[11]}}))
                else:
                    dets.append((row[0],{'AGR':{'PER':row[4],'NUM':row[6],'POSS':row[7],'INC': row[8], 'NAS':'N', 'PRES':row[11]}}))
                    dets.append((row[0],{'AGR':{'PER':row[4],'NUM':row[6],'POSS':row[7],'INC': row[8], 'NAS':'O', 'PRES':row[11]}}))
            found = True
    if not found:
        dets.append((tree['word'],{'AGR':{'NAS':nasal_spanish(tree['word']), 'INC':'I'}}))
        dets.append((tree['word'],{'AGR':{'NAS':nasal_spanish(tree['word']), 'INC':'E'}}))
        dets.append((tree['word'],{'AGR':{'INC':'I'}}))
        dets.append((tree['word'],{'AGR':{'INC':'E'}}))
    return dets

def nasal_spanish(verb):
    nasal = 'O'
    nasals = ['m', 'n', 'ñ', 'mb', 'nd', 'ng', 'nt']
    if any(nas in verb for nas in nasals):
        nasal = 'N' 
    return nasal