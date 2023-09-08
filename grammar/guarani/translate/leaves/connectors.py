def translate_connectors(tree,conCSV):
    conList = []
    con = tree['word']
    found = False
    for row in conCSV:
        if row[1].lower() == con.lower():
            conList.append((row[0],{'AGR':{}}))
            found = True
    if not found:
        conList.append((con,{'AGR':{}}))
    return conList