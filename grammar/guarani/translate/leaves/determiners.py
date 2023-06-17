def translate_determiners(tree,detCSV):
    dets = []
    label = tree['label']
    agreement = label['AGR']
    gen = agreement['GEN']
    num = agreement['NUM']
    typ = label['TYPE']
    possPer = label['POSSPER']
    possNum = label['POSSNUM']
    
    for row in detCSV:
        if row[12] == tree['word'] and row[15].lower() == typ.lower() and row[18].lower() == num.lower() and row[17].lower() == gen.lower() and row[16] == possPer and row[19] == possNum:
            dets.append({'det':row[0],'persona':row[4],'numero':row[6],'possesor':row[7],'incluyente': row[8], 'nasal':row[9], 'tercero':row[10],'presencia':row[11]})
    return dets