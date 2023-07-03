from collections import defaultdict
from translate.parsing.rule_to_cfg import rule_to_cfg
from translate.parsing.parse_rule import parse_rule
from .unification import UnificationFailed, unify
from .parse_lhs_feat import parse_lhs_features
from .replace_variables import replace_variables
from translate.leaves.translate_leaf import translate_leaf
from itertools import product, combinations
from copy import deepcopy

def cartesian_product(lists):
    return list(product(*lists))

def get_combinations(my_list):
    return list(combinations(my_list, 2))


def build_guarani_tree(spanish_tree, equivalence, lexicon):
    sp_rule = spanish_tree['type'] + ' ->'
    if (len(spanish_tree['children']) == 0):
        # return [sp_rule + ' ' + spanish_tree['word']]
        #return [] ### Actually need to take care of this case
                    # Should return a list of possible string-features pairs for this word
                    # Return type should be [(string, features)] where features is a dict
        # temp = translate_leaf(spanish_tree, lexicon)
        # print(temp)
        # return temp
        return translate_leaf(spanish_tree, lexicon)
    
    for child in spanish_tree['children']:
        sp_rule += ' ' + child['type']

    

    # For children get their subtree? Or just the word? Or maybe features and string?
    # Then use the guarani rule to select the order of those words
    # Hence we have something like the ordered guarani symbols, labels and words, and the rule
    # Using that we can apply unification, because for each symbol we'll have several
    # pairs of features and words to translate, and we'll have to unify those and return
    # a plausible set of features and strings associated with our main symbol at this step.

    translations = defaultdict(lambda: [])
    for child in spanish_tree['children']:
        translations[child['type']] += build_guarani_tree(child, equivalence, lexicon)
    # print('trans:')
    # print(translations)
    # print('end_trans')
    #  S-> NP VP
    # {NP: [(string, features)], VP: [(string, features)]}

    result = []

    gn_rules : str = equivalence[sp_rule] # This is a list of rules

    for gn_rule in gn_rules:
        cfg_gn_rule = rule_to_cfg(gn_rule)
        gn_symbol_translations = []
        right_hand_side = cfg_gn_rule.split('->')[1].strip().split()
        # [VP, NP]

        for symbol in right_hand_side:
            gn_symbol_translations.append((symbol, translations[symbol]))

        possibilities = cartesian_product([x[1] for x in gn_symbol_translations])

        rule_tree = parse_rule(gn_rule.split('->')[1].strip())
        # print(gn_rule)
        # print(rule_tree)
        lhs_features = parse_lhs_features(gn_rule.split('->')[0].strip())

        # Possibilities is a list of lists of tuples, where each tuple is (string, features)

        for possibility in possibilities:
            try:
                variables = {}
                for feat in rule_tree.keys():
                    for val in rule_tree[feat].keys():
                        matchings = rule_tree[feat][val]
                        should_match = get_combinations(matchings)
                        for (a, b) in should_match:
                            if (a != b):
                                unified = unify(possibility[a][1], possibility[b][1], feat)
                                if (unified == None):
                                    raise UnificationFailed("Unification failed")
                                
                        unified = possibility[matchings[0]][1] 
                        for i in range(1, len(matchings)):
                            unified = unify(unified, possibility[matchings[i]][1], feat) # Unified has shape {feat: unification_result}
                            if (unified == None):
                                raise UnificationFailed("Unification failed")
                        variables[val] = unified[feat]
                possibility_features = deepcopy(lhs_features)
                replace_variables(variables, possibility_features)
                strings = [x[0] for x in possibility]
                joint_string = ' '.join(strings)
                result.append((joint_string, possibility_features))

                        # Part of the old pseudocode:
                        # then unify their results (or maybe we can stack unifications from the beginning?)
                        # if cannot unify, discard the whole combination
                        # variables[val] = finalUnifiedResult
                        # Once we are done with those, we can use the variables dict and the lhs of the rule
                        # to create a new features dict corresponding to the whole sentence
                        # Finally, we append all strings in possibility and append the duple
                        # (string, features) to result
            except UnificationFailed as e:
                pass

    # print(result)
    return result


    # Pseudocode:
    # get cartesian product
    # parse rule
    # for each combination:
    #   for each step of rule:
    #       unify
    #       if unification fails:
    #           discard combination
    #       else:
    #           store unified result
    #   add combination to possibilities, with unified string and features
    
    # [(VP, [(string, features)]), (NP, [(string, features)])]
    

    # [(D, [(string, features)]), (N, traducciones)]

    # gn_rule = "NP[AGR=?a] -> D[AGR=?a, NAS=?b] N[AGR=?a, NAS=?b]" 

    # [(D, string, features), (N, string, features)]

    # [(string, features)]

    # [(string, features)]

    # So I should do the producto cartesiano of the aforementioned thing and 
    # unify on each step, so check the object for matches, first parsing the rule.
    # Seems not trivial but not too hard either.




    # for D:
    #     for N:
    #         parse (D N)



    ### New idea: use the NLTK parser on each step. Just place the words in the new order,
    ##  have our grammar, and ask it to parse away. Hence we can weed out invalid combinations.

    

    

    # for child in spanish_tree['children']:
    #     rules += build_guarani_tree(child, equivalence)
    # return rules













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