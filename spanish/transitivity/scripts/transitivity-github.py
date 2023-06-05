# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:25:12 2017

@author: Mirith

https://github.com/Mirith/Verb-categorizer/blob/master/transitivity.py

Info: listing verbs by transitivity

"""

###########################
# classifiying verbs based on transitivity
# list of all verbs by tokens

# for nlp and dataset
import spacy
from collections import defaultdict
import textacy

cw = textacy.corpora.CapitolWords()
nlp = spacy.load('en')

# all verbs found
totalVerbs = []
# set of unique verbs found, by lemma
unique = set([])

# takes a while to run bc nested for loops... like 30 min
for record in cw.records():
    # gets text of record
    text = record["text"]
    # processes the text of the record
    processed = nlp(text)
    
    # adds words to totalVerbs if they are verbs
    totalVerbs += [token for token in processed if (token.pos_ == "VERB")]
    
    # adding lemmas to the set
    for token in processed:
        if token.pos_ == "VERB":
            unique |= set([token.lemma_])

print(len(totalVerbs))
print(len(unique))
# totalVerbs should be greater than unique by a very large margin

# dictionaries -- verb:instances it is the given transitivity
# for intransitive verbs
intransitive = defaultdict(int)
# for transitive verbs
transitive = defaultdict(int)
# for ditransitive verbs
ditransitive = defaultdict(int)
# dictionary with words that didn't fit categories for some reason...
oops = defaultdict(int)

for verb in totalVerbs:
    # direct object check
    directObject = False
    # indirect object check
    indirectObject = False
    
    # looks through each verb's child ie dependents
    for item in verb.children:
        # sets indirectObject to true if indirect object is found
        if(item.dep_ == "iobj" or item.dep_ == "pobj"):
            indirectObject = True
        # sets directObject to true if direct object is found
        if (item.dep_ == "dobj" or item.dep_ == "dative"):
            directObject = True
            
    # both indirect and direct object ie ditransitive
    if (indirectObject == True) and (directObject == True):
        # increments proper lemma value by 1
        ditransitive[verb.lemma_] += 1
    # only direct object and no indirect object ie transitive
    elif (directObject == True) and (indirectObject == False):
        # increments proper lemma value by 1
        transitive[verb.lemma_] += 1
    # neither direct nor indirect object ie intransitive
    elif (directObject == False) and (indirectObject == False):
        # increments proper lemma value by 1
        intransitive[verb.lemma_] += 1
    else: 
        # increments proper lemma value by 1
        oops[verb.lemma_] += 1

###########################
# combining transitivities and getting proportions

# dictionary that combines verb transitivities
combined = defaultdict(list)

# goes through list of unique verbs and adds them to a dictionary 
# with a list of their transitivities
for verb in unique:
    toAdd = []

    toAdd.append(intransitive[verb])
    toAdd.append(transitive[verb])
    toAdd.append(ditransitive[verb])
    # dictionary of total occurences of verb in each transitivity
    # [intransitive, transitive, ditransitive]
    combined[verb] = toAdd

# for verbs that are listed but don't occur...?
# division by 0 occurs when they are encountered
problemVerbs = []

# turns list of transitivities into a 
# list of proportions of time verb is that transitivity
for verb in combined:
    
    occurences = 0
    
    # totaling the occurences of the verb in all transitivities
    for number in combined[verb]:
        occurences += number
    
    # making sure the verb occurs so no division by zero... 
    # which shouldn't be an issue but apparently is
    if occurences != 0:
        # calculates the percentage of times the verb occurs as a given transitivity
        # rounds to the third decimal place for neatness
        intransitiveProportion = round(float((combined[verb][0])/occurences) * 100, 3)
        transitiveProportion = round(float((combined[verb][1])/occurences) * 100, 3)
        ditransitiveProportion = round(float((combined[verb][2])/occurences) * 100, 3)
    else:
        problemVerbs.append(verb)
    
    # adding to the dictionary proportions
    # verb(lemma):transitivity(list)
    # list should hold proportion of times the verb occurs as each transitivity
    # and the total occurences of it in the text
    proportions = [intransitiveProportion, transitiveProportion,\
                   ditransitiveProportion, occurences]
    
    # setting the verb's entry in the dictionary equal to the correct proportions
    combined[verb] = proportions

###########################
# printing neat-ish results
for verb in combined:
    print("VERB:", verb, "--", combined[verb][3], "occurence(s)"\
    "\n\tIntransitive:", combined[verb][0], "% of the time"\
    "\n\tTransitive:", combined[verb][1], "% of the time"\
    "\n\tDitransitive:", combined[verb][2], "% of the time")
