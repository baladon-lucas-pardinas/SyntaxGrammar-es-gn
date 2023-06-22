from collections import defaultdict
from ..parsing.rule_to_cfg import rule_to_cfg


def build_guarani_tree(spanish_tree, equivalence):
    possibilities = []
    sp_rule = spanish_tree['type'] + ' ->'
    if (len(spanish_tree['children']) == 0):
        # return [sp_rule + ' ' + spanish_tree['word']]
        return [] ### Actually need to take care of this case
                    # Should return a list of possible string-features pairs for this word
                    # Return type should be [(string, features)] where features is a dict
    
    for child in spanish_tree['children']:
        sp_rule += ' ' + child['type']

    gn_rule = equivalence[sp_rule]
    cfg_gn_rule = rule_to_cfg(gn_rule)
    

    # For children get their subtree? Or just the word? Or maybe features and string?
    # Then use the guarani rule to select the order of those words
    # Hence we have something like the ordered guarani symbols, labels and words, and the rule
    # Using that we can apply unification, because for each symbol we'll have several
    # pairs of features and words to translate, and we'll have to unify those and return
    # a plausible set of features and strings associated with our main symbol at this step.

    translations = defaultdict(lambda: [])
    for child in spanish_tree['children']:
        translations[child['type']] += build_guarani_tree(child, equivalence)

    symbol_value_list = []
    right_hand_side = cfg_gn_rule.split('->')[1].strip().split()

    for symbol in right_hand_side:
        symbol_value_list.append((symbol, translations[symbol]))

    # [(D, [(string, features)]), (N, traducciones)]

    # gn_rule = "NP[AGR=?a] -> D[AGR=?a, NAS=?b] N[AGR=?a, NAS=?b]" 

    # [[(D, string, features)], [(N, string, features)]]

    # [(string, features)]

    # So I should do the producto cartesiano of the aforementioned thing and 
    # unify on each step, so check the object for matches, first parsing the rule.
    # Seems not trivial but not too hard either.




    # for D:
    #     for N:
    #         parse (D N)



    ### New idea: use the NLTK parser on each step. Just place the words in the new order,
    ##  have our grammar, and ask it to parse away. Hence we can weed out invalid combinations.

    

    

    for child in spanish_tree['children']:
        rules += build_guarani_tree(child, equivalence)
    return rules













# def build_guarani_tree(spanish_tree, equivalence):
#     rules = []
#     rule = spanish_tree['type'] + ' ->'
#     if (len(spanish_tree['children']) == 0):
#         return [rule + ' ' + spanish_tree['word']]
#     for child in spanish_tree['children']:
#         rule += ' ' + child['type']
#     rules.append(rule)
#     for child in spanish_tree['children']:
#         rules += build_guarani_tree(child, equivalence)
#     return rules