from fetch.spanish_trees import fetch_spanish_trees
from utils.read_csv import read_csv
from utils.parse_arguments import parse_arguments
from leaves.determiners import translate_determiners
from leaves.nouns import translate_nouns
from leaves.verbs import translate_verbs


    
def get_syntactic_transfer_rules(filepath):
    # dummy, I need to actually write the fetch function for this
    rules = {
        'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]' : 'S[AGR=?a] -> NP[AGR=?a] VP[AGR=?a, MOOD=i]',
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='intr']",
        "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr'] NP[AGR=?b]" : "VP[AGR=?a, MOOD=?m] -> V[AGR=?a, MOOD=?m, SUBCAT='tr']",
        "NP[AGR=?a] -> D[AGR=?a] N[AGR=?a]" : "NP[AGR=?a, NAS=?b] -> D[AGR=?a, NAS=?b] N[AGR=?a, NAS=?b]",
    }
    return rules

def main():
    # Get CSV files
    nouns = read_csv("../../../guarani/nouns/finished-nouns.csv")
    determiners = read_csv("../../../guarani/determiners/determiners.csv")
    adjectives = read_csv("../../../guarani/adjectives/matched-adjectives-guarani.csv")
    pronouns = read_csv("../../../guarani/pronouns/pronouns.csv")
    verbs = read_csv("../../../guarani/verbs/matched-verbs-guarani.csv")

    args = parse_arguments()
    trees = fetch_spanish_trees(args.spanish_trees_file)

    ### Rubbish
    ## nouns:
    #x = trees[0]['children'][0]['children'][1]
    ## verbs:
    #x = trees[0]['children'][1]['children'][0]
    ## determiners:
    x = trees[0]['children'][0]['children'][0]
    print(x)
    y = translate_determiners(x, determiners)
    print(y)
    ### End of rubbish

    ### Next steps: 
    # get equivalent grammar rules
    # get equivalent lexicon rules
    # perform transformation on tree, rule by rule, top to bottom
    # consolidate guarani sentence
    # write both sentences in parallel as a csv

if __name__ == '__main__':
    main()