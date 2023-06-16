import argparse
import csv
import re

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('spanish_trees_file', type=str, help='Path to the spanish trees file')
    parser.add_argument('equivalence_rules_file', type=str, help='Path to the equivalence rules file')
    parser.add_argument('-o', '--output', type=str, default='output.txt', help='Path to the output file')

    return parser.parse_args()

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix
    
def get_syntactic_transfer_rules(filepath):
    # dummy
    rules = {
        'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]' : 'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]',
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']",
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP[AGR=?b]" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr']",
        "NP[AGR=?a] -> D[AGR=?a] N[AGR=?a]" : "NP[AGR=?a, NAS=?b] -> D[AGR=?a, NAS=?b] N[AGR=?a, NAS=?b]",
    }
    return rules

# def parse_tree(tree_str):
#     stack = []
#     current_node = None
#     principio = False
#     termino = False

#     for char in tree_str:
#         if char == "(":
#             if current_node is not None:
#                 stack.append(current_node)
#             current_node = {'type': '', 'label': '', 'children': [], 'word': ''}
#             principio = True
#             termino = False
#         elif char == ")":
#             if stack:
#                 parent_node = stack.pop()
#                 parent_node['children'].append(current_node)
#                 current_node = parent_node
#                 termino = False
#         elif char == "[":
#             termino = False
#             principio = False
#         elif char == "]":
#             termino = True
#         else:
#             if principio and not str.isspace(char):
#                 current_node['type'] += char
#             elif termino and not str.isspace(char):
#                 if char == ',':
#                     current_node['label'] += char
#                     termino = False
#                 else:
#                     current_node['word'] += char
#             elif not str.isspace(char):
#                 current_node['label'] += char

#     return current_node
def parse_tree(tree_str):
    stack = []
    current_node = None
    principio = False
    termino = False

    for char in tree_str:
        if char == "(":
            if current_node is not None:
                stack.append(current_node)
            current_node = {'type': '', 'label': '', 'children': [], 'word': ''}
            principio = True
            termino = False
        elif char == ")":
            if stack:
                parent_node = stack.pop()
                parent_node['children'].append(current_node)
                current_node = parent_node
                termino = False
        elif char == "[":
            termino = False
            principio = False
            current_node['label'] += char  # Include the square bracket in the label
        elif char == "]":
            termino = True
            current_node['label'] += char  # Include the square bracket in the label
        else:
            if principio and not str.isspace(char):
                current_node['type'] += char
            elif termino and not str.isspace(char):
                if char == ',':
                    current_node['label'] += char
                    termino = False
                else:
                    current_node['word'] += char
            elif not str.isspace(char):
                current_node['label'] += char

    return current_node

def parse_nested_dict(string):
    stack = []
    current_dict = {}
    key = ""
    value = ""
    inside_quotes = False

    for char in string:
        if char == "[":
            if key:
                stack.append((key, current_dict))
                current_dict = {}
                key = ""
        elif char == "]":
            if key:
                current_dict[key] = value.strip()
                key = ""
                value = ""
            if stack:
                parent_key, parent_dict = stack.pop()
                parent_dict.update(current_dict)
                current_dict = parent_dict
        elif char == "=":
            if inside_quotes:
                value += char
            else:
                key = value.strip()
                value = ""
        elif char == ",":
            if inside_quotes:
                value += char
            else:
                current_dict[key] = value.strip()
                key = ""
                value = ""
        elif char == "'":
            inside_quotes = not inside_quotes
        else:
            value += char

    return current_dict


def get_spanish_trees(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

        trees = []
        tree_start = -1
        stack = []

        for i, char in enumerate(content):
            if char == '(':
                if not stack:
                    tree_start = i
                stack.append('(')
            elif char == ')':
                if len(stack) == 1:
                    trees.append(content[tree_start:i+1])
                stack.pop()

    # Should apply parse_nested_dict to each tree's label I believe
    return [parse_tree(x) for x in trees]

def translate_nouns(tree,nounCSV):
    nounsRes = []
    genExp = r'.*GEN=?\'(.)\'.*' 
    numExp = r'.*NUM=?\'(.)\'.*' 
    gen = re.search(genExp,tree['label']).group(1)
    num = re.search(numExp,tree['label']).group(1)
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
    nouns = read_csv("../../guarani/nouns/finished-nouns.csv")
    determiners = read_csv("../../guarani/determiners/determiners.csv")
    adjectives = read_csv("../../guarani/adjectives/matched-adjectives-guarani.csv")
    pronouns = read_csv("../../guarani/pronouns/pronouns.csv")
    verbs = read_csv("../../guarani/verbs/matched-verbs-guarani.csv")

    args = parse_arguments()
    trees = get_spanish_trees(args.spanish_trees_file)
    x = trees[0]['children'][1]['children'][0]
    print(x)
    y = translate_verbs(x, verbs)
    print(y)
    
    ### Next steps: 
    # get equivalent grammar rules
    # get equivalent lexicon rules
    # perform transformation on tree, rule by rule, top to bottom
    # consolidate guarani sentence
    # write both sentences in parallel as a csv

if __name__ == '__main__':
    main()