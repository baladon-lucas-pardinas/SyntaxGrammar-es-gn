import os
import xml.etree.ElementTree as ET
import csv

def write_to_csv(filepath, rows):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)

def recorrerAncoraVerbs(ruta):
    pre = []
    etiquetas = []

    # bucle a través de todos los archivos en la carpeta
    for archivo in os.listdir(ruta):
        # si el archivo tiene extensión .xml, procesarlo
        if archivo.endswith(".xml"):
            # parsear el archivo xml
            arbol = ET.parse(os.path.join(ruta, archivo))
            raiz = arbol.getroot()
            lemma = raiz.attrib['lemma']
            frameList = raiz.findall('./sense/frame')
            for frame in frameList:
                existe = frame.attrib.__contains__('lss')
                if existe:
                    existe2 = (frame.attrib.__contains__('type') and frame.attrib['type'] == 'default') or (frame.attrib.__contains__('default') and frame.attrib['default'] == 'yes')
                    funcList = []
                    if not frame.attrib['lss'] in etiquetas:
                        etiquetas.append(frame.attrib['lss'])
                    argumentList = frame.findall('./argument')
                    for arg in argumentList:
                        funcList.append(arg.attrib['function'])
                    if existe2:
                        pre.append([lemma, frame.attrib['lss']]+funcList)


    #print(etiquetas)
    return pre

def process2(verbs):
    post = []
    unresolved = []

    for v in verbs:
        tag = v[1].split('.')[0]
        if ('ci' in v[2:]) and ('cd' in v[2:]):
            post.append([v[0],'ditransitive'])
        elif ('cd' in v[2:]) and not ('ci' in v[2:]):
            post.append([v[0],'transitive'])
        elif not ('cd' in v[2:]) and not ('ci' in v[2:]):
            post.append([v[0],'intransitive'])
        else:
            unresolved.append(v)
    return post, unresolved

def unir(verbos):
    ultimoVerbo = ''
    filas = []
    ultimaFila = []
    for v in verbos:
        if v[0] == ultimoVerbo:
            if not v[1] in ultimaFila:
                ultimaFila.append(v[1])
        else:
            if (len(ultimaFila) > 0):
                filas.append(ultimaFila)
            ultimoVerbo = v[0]
            ultimaFila = [v[0],v[1]]
    return filas

def formato(verbos):
    rows = []
    tr = ''
    di = ''
    intr = ''
    for v in verbos:
        if 'transitive' in v:
            tr = 'tr'
        else: 
            tr = '0'
        if 'ditransitive' in v:
            di = 'di'
        else: 
            di = '0'
        if 'intransitive' in v:
            intr = 'intr'
        else: 
            intr = '0'
        rows.append([v[0],tr,di,intr])
    return rows

def main():
    ruta = "../../ancoralex-es-2.0.3/ancora-verb-es"  # reemplazar con la ruta de la carpeta que contiene los archivos xml
    final = recorrerAncoraVerbs(ruta)
    write_to_csv("ancora-verbs.csv", final)
    (post, unresolver) = process2(final)
    merged = unir(post)
    conFormato = formato(merged)
    print(conFormato)
    #print(post)
    #write_to_csv("postancora-verbs.csv", post)
    write_to_csv("merged-transitivity.csv",merged)
    write_to_csv("final-transitivity.csv",conFormato)
    write_to_csv("unresolverancora-verbs.csv", unresolver)

main()
