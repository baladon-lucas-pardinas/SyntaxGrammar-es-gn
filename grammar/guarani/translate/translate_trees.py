from .fetch.spanish_trees import fetch_spanish_trees
from .utils.read_csv import read_csv
from .utils.write_csv import write_to_csv
from .utils.parse_arguments import parse_arguments
from .corpus_generation.remove_duplicates import remove_duplicates
from .leaves.determiners import translate_determiners
from .leaves.nouns import translate_nouns
from .leaves.verbs import translate_verbs
from .transfer.guarani_tree import build_guarani_tree
from .corpus_generation.extract_words import extract_words
from .corpus_generation.post_process import post_process

    
def get_syntactic_transfer_rules(filepath):
    # dummy, I need to actually write the fetch function for this
    # These actually need to be lists of possible equivalent rules
    rules = {
        # 'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]' : 'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]',
        # "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']",
        # "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP[AGR=?b]" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr']",
        # "NP[AGR=?a] -> D[AGR=?a] N[AGR=?a]" : "NP[AGR=?a, NAS=?b] -> D[AGR=?a, NAS=?b] N[AGR=?a, NAS=?b]",'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]' : 'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]',
        "S -> NP VP PP" : ["S[AGR='?a'] -> NP[AGR='?a'] VP[AGR='?a'] PP"],
        "S -> NP VP" : ["S[AGR='?a'] -> NP[AGR='?a'] VP[AGR='?a']"],

        "S -> P VP PP" : ["S[AGR='?a'] -> P[AGR=[INC='?i', POS='b'], CASE='n'] VP[AGR=[INC='?i', POS='b']] PP",
                        "S[AGR='?a'] -> P[AGR=[INC='?i', POS=0], CASE='n'] VP[AGR=[INC='?i', POS=0]] PP",
                        "S[AGR='?a'] -> VP[AGR=[INC='?i', POS='b']] P[AGR=[INC='?i', POS='b'], CASE='n'] PP",
                        "S[AGR='?a'] -> VP[AGR=[INC='?i', POS='p']] P[AGR=[INC='?i', POS='p'], CASE='n'] PP"],

        "S -> P VP" : ["S[AGR='?a'] -> P[AGR=[INC='?i', POS='b'], CASE='n'] VP[AGR=[INC='?i', POS='b']]",
                    "S[AGR='?a'] -> P[AGR=[INC='?i', POS=0], CASE='n'] VP[AGR=[INC='?i', POS=0]]",
                    "S[AGR='?a'] -> VP[AGR=[INC='?i', POS='b']] P[AGR=[INC='?i', POS='b'], CASE='n']",
                    "S[AGR='?a'] -> VP[AGR=[INC='?i', POS='p']] P[AGR=[INC='?i', POS='p'], CASE='n']"],

        "VP -> V" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='intr', NEG=0]"],
        "VP -> V NP" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='tr', NEG=0] NP"],
        "VP -> V NP PPA" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='di', NEG=0] NP PPA"],
        # "VP -> V NP1 AA NP2" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='di', NEG=0] NP1 NP2[AGR='?a'] AA[AGR='?a']"],

        "VP -> NEG V" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='intr', NEG=1]"],
        "VP -> NEG V NP" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='tr', NEG=1] NP"],
        "VP -> NEG V NP PPA" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='di', NEG=1] NP PPA"],
        # "VP -> NEG V NP1 AA NP2" : ["VP[AGR='?a'] -> V[AGR='?a', SUBCAT='di', NEG=1] NP1 NP2[AGR='?a'] AA[AGR='?a']"],


        "PPA -> AA NP" : ["PPA[AGR='?a'] -> NP[AGR='?a', NW='?n'] AA[NW='?n']"],

        # "AA -> 'a'" : ["AA[AGR=[NAS='o']] -> '_pe'",
        #             "AA[AGR=[NAS='n']] -> '_me'"],

        "NP -> D N" : ["NP[AGR='?a', NW='?n'] -> D[AGR='?a'] N[AGR='?a', NW='?n']"],

        "PP -> PR NP" : ["PP -> NP[AGR='?a'] PR[AGR='?a', S='s']",
                        "PP -> NP[AGR='?a'] PR[AGR='?a', S='0']"],

        # "NEG -> 'no'" : [],
    }
    return rules

def main():
    # Get CSV files
    nouns = read_csv("../../guarani/nouns/finished-nouns.csv")
    determiners = read_csv("../../guarani/determiners/determiners.csv")
    adjectives = read_csv("../../guarani/adjectives/matched-adjectives-guarani.csv")
    pronouns = read_csv("../../guarani/pronouns/pronouns.csv")
    verbs = read_csv("../../guarani/verbs/matched-verbs-guarani.csv")
    adpositions = read_csv("../../guarani/adpositions/adpositions.csv")

    lexicon = {
        'N' : nouns,
        'D' : determiners,
        'A' : adjectives,
        'P' : pronouns,
        'V' : verbs,
        'AA': adpositions,
        'PR': adpositions
    }

    args = parse_arguments()
    trees = fetch_spanish_trees(args.spanish_trees_file)
    transfer_rules = get_syntactic_transfer_rules(args.equivalence_rules_file)
    # print(trees[26])
    #build_guarani_tree(trees[26], transfer_rules, lexicon)
    # print(trees[0])

    final = []

    for t in trees:
        aux = build_guarani_tree(t, transfer_rules, lexicon)
        p = extract_words(t)
        for (a,b) in aux:
            f = post_process([p,a])
            final.append(f)
    write_to_csv(args.output, final)
    remove_duplicates(args.output)


    ### Rubbish
    # x = trees[0]['children'][1]['children'][0]
    # print(x)
    # y = translate_verbs(x, verbs)
    # print(y)
    # print(trees[0])
    ## nouns:
    #x = trees[0]['children'][0]['children'][1]
    ## verbs:
    #x = trees[0]['children'][1]['children'][0]
    ## determiners:
    # x = trees[0]['children'][0]['children'][0]
    # print(x)
    # y = translate_determiners(x, determiners)
    # print(y)

    ### End of rubbish

    ### Next steps: 
    # get equivalent grammar rules
    # get equivalent lexicon rules
    # perform transformation on tree, rule by rule, top to bottom
    # consolidate guarani sentence
    # write both sentences in parallel as a csv

if __name__ == '__main__':
    main()