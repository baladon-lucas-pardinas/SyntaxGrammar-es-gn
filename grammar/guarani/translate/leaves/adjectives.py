def translate_adjectives(tree,adjCSV):
    adjList = []
    adj = tree['word']
    label = tree['label']
    agreement = label['AGR']
    num = agreement['NUM']
    try:
        gen = agreement['GEN']
    except:
        gen = 'C'
    found = False
    for row in adjCSV:
        if row[4].lower() == adj.lower() and row[9].lower() == gen.lower() and row[10].lower() == num.lower():
            adjList.append((row[0],{'AGR':{}}))
            found = True
    if not found:
        adjList.append((adj,{'AGR':{}}))
    return adjList