### Read: https://www.nltk.org/book/ch09.html
import csv


def write_noun_productions(grammar_file, noun_lexicon):
    # Load noun lexical rules from CSV
    with open(noun_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            shifted_row = ["dummy"] + row
            word = shifted_row[1]
            gender = shifted_row[5]
            number = shifted_row[6]

            agr_feats = "PER=3"
            if (gender != "C"):
                agr_feats += f", GEN={gender.lower()}"

            num_feats = [f", NUM={number.lower()}"]
            if (number == "N"):
                num_feats = [f", NUM={num.lower()}" for num in ["S", "P"]]

            for num_feat in num_feats:
                grammar_file.write(f"N[AGR=[{agr_feats + num_feat}]] -> '{word}'\n")
