def translate_determiners(tree,detCSV):
    dets = []
    label = tree['label']
    agreement = label['AGR']
    gen = agreement['GEN']
    num = agreement['NUM']
    typ = label['TYPE']
    possPer = label['POSSPER']
    possNum = label['POSSNUM']
    
    ## Tener cuidado de solo mirar TER cuando se conjuga en tercera persona
    ## Actualmente la presencia (PRES) no se utiliza
    for row in detCSV:
        if row[12] == tree['word'] and row[15].lower() == typ.lower() and row[18].lower() == num.lower() and row[17].lower() == gen.lower() and row[16] == str(possPer) and row[19] == str(possNum):
            dets.append((row[0],{'AGR':{'PER':row[4],'NUM':row[6],'POSS':row[7],'INC': row[8], 'NAS':row[9], 'TER':row[10],'PRES':row[11]}}))
    return dets