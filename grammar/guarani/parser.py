import csv
import re

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def read_csv(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        matrix = []
        for row in reader:
            matrix.append(row)
        return matrix
    
def processTxt(archivo):
    resultado = []
    linea = ''
    h = 'Hola'
    for l in archivo:
        if (str(l).startswith('(S')):
            resultado.append(linea)
            linea = []
            linea.append(l)
        else:
            linea.append(l)
    return resultado

def main():
    archivo = open("../grammar-files/g3/trees.txt", 'r')
    res = processTxt(archivo)
    archivo.close()

    file1 = open("myfile.txt","w")#write mode
    for r in res:
        for x in r:
            file1.write(x)
    file1.close()

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
        elif char == "]":
            termino = True
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


def translate_tree(tree):
    """ word_mapping = {
        'nosotras': 'che resẽ',
        'lisiaríamos': 'ambyai',
        'nuestras': 'che rupi',
        'olas': 'mba\'e',
        # Otros mapeos de palabras necesarios para la traducción al guaraní
    }

    tag_mapping = {
        'S -> NP VP': 'S -> NP VP',
        'VP -> VP': 'VP -> VP',
        'VP': 'V',
        'V': 'V',
        'NP': 'D N',
        'D': 'D',
        'N': 'N'
        # Otros mapeos de etiquetas necesarios para la traducción al guaraní
    } """

    genExp = r'.*GEN=?\'(.)\'.*' 
    numExp = r'.*NUM=?\'(.)\'.*' 
    perExp = r'.*PER=?\'(.)\'.*' 

    match tree['type']:
        case 'N':
            gen = re.search(tree['label'],genExp).group(1)
            num = re.search(tree['label'],numExp).group(1)
            for row in nouns:
                if row[6] == tree['word'] and row[10] == gen and row[11] == num:
                    nouns.append(row[0])

    translated_tree = {'label': tag_mapping.get(tree['label'], tree['label']), 'children': []}
    if 'children' in tree:
        for child in tree['children']:
            translated_child = translate_tree(child)
            translated_tree['children'].append(translated_child)

    if 'word' in tree:
        translated_word = word_mapping.get(tree['label'], tree['label'])
        translated_tree['label'] = translated_word

    return translated_tree

def translate_nouns(tree):
    nouns = []
    genExp = r'.*GEN=?\'(.)\'.*' 
    numExp = r'.*NUM=?\'(.)\'.*' 
    gen = re.search(tree['label'],genExp).group(1)
    num = re.search(tree['label'],numExp).group(1)
    for row in nouns:
        if row[6] == tree['word'] and row[12].lower() == gen.lower() and row[13].lower() == num.lower():
            nouns.append({'noun':row[0], 'tercera':row[6], 'nasal':row[7]})
    return nouns

def translate_det(tree):
    nouns = []
    genExp = r'.*GEN=?\'(.)\'.*' 
    numExp = r'.*NUM=?\'(.)\'.*' 
    typeExp = r'.*TYPE=?\'(.)\'.*' 
    possPerExp = r'.*POSSPER=0=?\'(.)\'.*' 
    possNumExp = r'.*POSSNUM=0=0=?\'(.)\'.*' 
    gen = re.search(tree['label'],genExp).group(1)
    num = re.search(tree['label'],numExp).group(1)
    typ = re.search(tree['label'],typeExp).group(1)
    possPer = re.search(tree['label'],possPerExp).group(1)
    possNum = re.search(tree['label'],possNumExp).group(1)
    for row in nouns:
        if row[6] == tree['word'] and row[16].lower() == typ.lower() and row[19].lower() == num.lower() and row[18].lower() == gen.lower() and row[17].lower() == possPer.lower() and row[20].lower() == possNum.lower():
            nouns.append({'det':row[0],'persona':row[4],'numero':row[6],'possesor':row[7],'incluyente': row[8], 'nasal':row[9], 'tercero':row[10],'presencia':row[11]})
    return nouns

def translate_verbs(tree):
    verbs = []
    numExp = r'.*NUM=?\'(.)\'.*' 
    perExp = r'.*PER=?\'(.)\'.*' 
    tenseExp = r'.*TENSE=?\'(.)\'.*' 
    moodExp = r'.*MOOD=?\'(.)\'.*' 
    mood = re.search(tree['label'],moodExp).group(1)
    tense = re.search(tree['label'],tenseExp).group(1)
    per = re.search(tree['label'],perExp).group(1)
    num = re.search(tree['label'],numExp).group(1)
    for row in nouns:
        if row[12] == tree['word'] and row[16].lower() == mood.lower() and row[17].lower() == tense.lower() and row[18] == per and row[19].lower() == num.lower():
            verbs.append([row[0],row[7],row[8]])


def translate_tree2(tree):
    word_mapping = {
        'nosotras': 'che resẽ',
        'lisiaríamos': 'ambyai',
        'nuestras': 'che rupi',
        'olas': 'mba\'e',
        # Otros mapeos de palabras necesarios para la traducción al guaraní
    }

    tag_mapping = {
        'S ': 'NP VP',
        'P ': 'NP VP',
        'VP': 'V',
        'V ': 'V',
        'NP': 'D N',
        'D ': 'D',
        'N ': 'N'
        # Otros mapeos de etiquetas necesarios para la traducción al guaraní
    }

    #print(tree['label'])
    translated_tree = {'type': tag_mapping.get(tree['type'], tree['type']), 'children': []}
    print(translated_tree)
    if 'children' in tree:
        for child in tree['children']:
            translated_child = translate_tree(child)
            translated_tree['children'].append(translated_child)

    if 'word' in tree:
        translated_word = word_mapping.get(tree['word'], tree['word'])
        translated_tree['word'] = translated_word

    return translated_tree


nouns = read_csv("../../guarani/nouns/finished-nouns.csv")
determiners = read_csv("../../guarani/determiners/determiners.csv")
adjectives = read_csv("../../guarani/adjectives/matched-adjectives-guarani.csv")
pronouns = read_csv("../../guarani/pronouns/pronouns.csv")
verbs = read_csv("../../guarani/verbs/matched-verbs-guarani.csv")

# Árbol gramatical en español
#tree_str = "(S[AGR=[GEN='f', NUM='p', PER=1, TENSE='c']] (P[AGR=[GEN='f', NUM='p', PER=1], CASE='n', POLITE=0, TYPE='p'] nosotras) (VP[AGR=[NUM='p', PER=1, TENSE='c'], MOOD='i'] (V[AGR=[NUM='p', PER=1, TENSE='c'], MOOD='i', SUBCAT='tr'] lisiaríamos) (NP[AGR=[GEN='f', NUM='p', PER=3]] (D[AGR=[GEN='f', NUM='p'], POSSNUM='p', POSSPER=1, TYPE='p'] nuestras) (N[AGR=[GEN='f', NUM='p', PER=3]] olas))))"
with open('../grammar-files/g3/trees.txt', 'r') as file:
    tree_str = file.read()

tree_str = tree_str.replace('\n', '')  # Eliminar saltos de línea
tree_str = tree_str.replace(')(', ')\n(')  # Agregar salto de línea después de cada árbol

with open('archivo_reformateado.txt', 'w') as archivo_salida:
    archivo_salida.write(tree_str)

file1 = open('archivo_reformateado.txt', 'r')
Lines = file1.readlines()
# Parsear el árbol gramatical
contador = 1
for i in Lines:
    parsed_tree = parse_tree(i)
    #print(parsed_tree)
    print(parsed_tree)
    print(contador)
    contador += 1

# Traducir el árbol al guaraní
translated_tree = translate_tree(parsed_tree)

# Imprimir el árbol traducido
import json
#print(json.dumps(translated_tree, ensure_ascii=False, indent=2))
