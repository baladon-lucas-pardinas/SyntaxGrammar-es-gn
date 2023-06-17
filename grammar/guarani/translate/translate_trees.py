import re
from fetch.spanish_trees import fetch_spanish_trees
from utils.read_csv import read_csv
from utils.parse_arguments import parse_arguments


    
def get_syntactic_transfer_rules(filepath):
    # dummy
    rules = {
        'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]' : 'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]',
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']",
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP[AGR=?b]" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr']",
        "NP[AGR=?a] -> D[AGR=?a] N[AGR=?a]" : "NP[AGR=?a, NAS=?b] -> D[AGR=?a, NAS=?b] N[AGR=?a, NAS=?b]",
    }
    return rules



def translate_nouns(tree,nounCSV):
    nounsRes = []
    genExp = r'.*GEN=?\'(.)\'.*' 
    numExp = r'.*NUM=?\'(.)\'.*' 
    gen = re.search(genExp,tree['labe']).group(1)
    num = re.search(numExp,tree['labell']).group(1)
    for row in nounCSV:
        if row[8] == tree['word'] and row[12].lower() == gen.lower() and row[13].lower() == num.lower():
            nounsRes.append({'noun':row[0], 'tercera':row[6], 'nasal':row[7]})
    return nounsRes

def translate_det(tree,detCSV):
    dets = []
    genExp = r'.*GEN=?\'(.)\'.*' 
    numExp = r'.*NUM=?\'(.)\'.*' 
    typeExp = r'.*TYPE=?\'(.)\'.*' 
    possPerExp = r'.*POSSPER=?(.).*' 
    possNumExp = r'.*POSSNUM=?(.).*' 
    print(tree)
    print(tree['label'])
    gen = re.search(genExp,tree['label']).group(1)
    num = re.search(numExp,tree['label']).group(1)
    typ = re.search(typeExp,tree['label']).group(1)
    possPer = re.search(possPerExp,tree['label']).group(1)
    possNum = re.search(possNumExp,tree['label']).group(1)
    for row in detCSV:
        if row[12] == tree['word'] and row[15].lower() == typ.lower() and row[18].lower() == num.lower() and row[17].lower() == gen.lower() and row[16] == possPer and row[19] == possNum:
            dets.append({'det':row[0],'persona':row[4],'numero':row[6],'possesor':row[7],'incluyente': row[8], 'nasal':row[9], 'tercero':row[10],'presencia':row[11]})
    return dets

def translate_verbs(tree,verbCSV):
    verbs = []
    numExp = r'.*NUM=?\'(.)\'.*' 
    perExp = r'.*PER=?(.).*' 
    tenseExp = r'.*TENSE=?\'(.)\'.*' 
    moodExp = r'.*MOOD=?\'(.)\'.*' 
    mood = re.search(moodExp,tree['label']).group(1)
    tense = re.search(tenseExp,tree['label']).group(1)
    per = re.search(perExp,tree['label']).group(1)
    num = re.search(numExp,tree['label']).group(1)
    for row in verbCSV:
        if row[12] == tree['word'] and row[16].lower() == mood.lower() and row[17].lower() == tense.lower() and row[18] == per and row[19].lower() == num.lower():
            verbs.append({'verbo':row[0],'inclusion':row[7],'posicion':row[8]})

def main():
    # Get CSV files
    nouns = read_csv("../../../guarani/nouns/finished-nouns.csv")
    determiners = read_csv("../../../guarani/determiners/determiners.csv")
    adjectives = read_csv("../../../guarani/adjectives/matched-adjectives-guarani.csv")
    pronouns = read_csv("../../../guarani/pronouns/pronouns.csv")
    verbs = read_csv("../../../guarani/verbs/matched-verbs-guarani.csv")

    args = parse_arguments()
    trees = fetch_spanish_trees(args.spanish_trees_file)
    # x = trees[0]['children'][1]['children'][0]
    # print(x)
    # y = translate_verbs(x, verbs)
    # print(y)
    print(trees[0])
    
    ### Next steps: 
    # get equivalent grammar rules
    # get equivalent lexicon rules
    # perform transformation on tree, rule by rule, top to bottom
    # consolidate guarani sentence
    # write both sentences in parallel as a csv

if __name__ == '__main__':
    main()