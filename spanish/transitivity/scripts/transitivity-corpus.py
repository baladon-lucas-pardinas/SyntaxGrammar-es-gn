import spacy
from collections import defaultdict

nlp = spacy.load("es_core_news_lg")
corpus = open("corpus.txt", encoding="utf-8").read()
processed = nlp(corpus)

total_verbs = []
unique_verbs = set()

for token in processed:
    if token.pos_ == "VERB":
        total_verbs.append(token)
        unique_verbs.add(token.lemma_)

intransitive = defaultdict(int)
transitive = defaultdict(int)
ditransitive = defaultdict(int)
oops = defaultdict(int)

for i in set(total_verbs):
    print(i)
    for j in i.children:
        print(j.text, j.dep_)
    print("-----")

for verb in total_verbs:
    direct_object = False
    indirect_object = False

    for child in verb.children:
        if child.dep_ == "iobj":
            indirect_object = True
        if child.dep_ == "obj":
            direct_object = True

    if indirect_object and direct_object:
        ditransitive[verb.lemma_] += 1
    elif direct_object and not indirect_object:
        transitive[verb.lemma_] += 1
    elif not direct_object and not indirect_object:
        intransitive[verb.lemma_] += 1
    else:
        oops[verb.lemma_] += 1

combined = defaultdict(list)
for verb in unique_verbs:
    to_add = [
        intransitive[verb],
        transitive[verb],
        ditransitive[verb]
    ]
    combined[verb] = to_add

with open("results.txt", "w", encoding="utf-8") as f:
    for verb, transitivity in combined.items():
        occurrences = sum(transitivity)
        if occurrences != 0:
            intransitive_proportion = round(transitivity[0] / occurrences, 3)
            transitive_proportion = round(transitivity[1] / occurrences, 3)
            ditransitive_proportion = round(transitivity[2] / occurrences, 3)
            f.write(f"{verb},{intransitive_proportion:.2f},{transitive_proportion:.2f},{ditransitive_proportion:.2f}\n")
        else:
            f.write(f"{verb},0.00,0.00,0.00\n")
