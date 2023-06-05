# # import spacy
# # nlp = spacy.load('es_core_news_lg') # load pre-built Spanish language model

# # verbs = ['hablar', 'comer', 'vivir', 'decir'] # list of infinitive verbs to process

# # with open('verbs.csv', 'w', encoding='utf-8') as f:
# #     f.write('verb,transitivity\n')
# #     for verb in verbs:
# #         doc = nlp(f'Al hombre le gusta {verb} la comida') # add a noun to create a sentence to parse
# #         for token in doc:
# #             if token.pos_ == 'VERB':
# #                 transitivity = token.dep_
# #                 f.write(f'{verb},{transitivity}\n')

# import spacy
# import csv

# # Load the Spanish model
# nlp = spacy.load('es_core_news_lg')

# # Read in the list of verbs from the csv file
# with open('../spanish-verbs/matched-verbs.csv', 'r') as f:
#     reader = csv.reader(f)
#     verbs = list(reader)

# print("read OK")

# transitivities = dict.fromkeys([x[2] for x in verbs])
# for key in transitivities.keys():
#     transitivities[key] = {'intrans': 0, 'trans': 0, 'bitrans': 0}


# # Iterate through the list of verbs
# for verb in verbs:
#     # Extract the infinitive form of the verb from the csv file
#     infinitive = verb[2]

#     form = verb[1]
#     # Parse the form with the Spanish model
#     doc = nlp(form)
    
#     # Check if the verb is intransitive
#     if any(token.dep_ == 'nsubj' for token in doc):
#         transitivities[infinitive]['intrans'] += 1
#     # Check if the verb is transitive
#     elif any(token.dep_ == 'nsubj' and any(child.dep_ == 'obj' for child in token.children) for token in doc):
#         transitivities[infinitive]['trans'] += 1
#     # Check if the verb is bitransitive
#     elif any(token.dep_ == 'nsubj' and any(child.dep_ == 'iobj' for child in token.children) and any(child.dep_ == 'obj' for child in token.children) for token in doc):
#         transitivities[infinitive]['bitrans'] += 1
#     print(infinitive + ','.join([str(i) for i in transitivities[infinitive].values()]))

# # Write the results to a csv file
# with open('results.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for verb, probas in transitivities:
#         values = [str(probas['intrans']), str(probas['trans']), str(probas['bitrans'])]
#         entry = verb + ',' + ','.join(values)
#         writer.writerow(entry)
