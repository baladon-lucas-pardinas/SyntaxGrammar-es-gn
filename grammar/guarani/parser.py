import csv
import xml.etree.ElementTree as ET

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
    word_mapping = {
        'nosotras': 'che resẽ',
        'lisiaríamos': 'ambyai',
        'nuestras': 'che rupi',
        'olas': 'mba\'e',
        # Otros mapeos de palabras necesarios para la traducción al guaraní
    }

    tag_mapping = {
        'S': 'NP VP',
        'P': 'NP VP',
        'VP': 'V',
        'V': 'V',
        'NP': 'D N',
        'D': 'D',
        'N': 'N'
        # Otros mapeos de etiquetas necesarios para la traducción al guaraní
    }

    translated_tree = {'label': tag_mapping.get(tree['label'], tree['label']), 'children': []}
    if 'children' in tree:
        for child in tree['children']:
            translated_child = translate_tree(child)
            translated_tree['children'].append(translated_child)

    if 'word' in tree:
        translated_word = word_mapping.get(tree['label'], tree['label'])
        translated_tree['label'] = translated_word

    return translated_tree


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
