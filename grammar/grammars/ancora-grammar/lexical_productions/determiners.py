### Read: https://www.nltk.org/book/ch09.html
import csv


def write_determiner_productions(grammar_file, determiner_lexicon):
    # Load determiner lexical rules from CSV
    with open(determiner_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[0]
            type = row[3].lower()
            possessor_person = row[4].lower()
            gender = row[5].lower()
            number = row[6].lower()
            possessor_num = row[7].lower()

            agr_feats = "PER=3"
            if (gender != "C"):
                agr_feats += f", GEN={gender.lower()}"

            num_feats = [f", NUM={number.lower()}"]
            if (number == "N"):
                num_feats = [f", NUM={num.lower()}" for num in ["S", "P"]]

            for num_feat in num_feats:
                grammar_file.write(f"D[AGR=[{agr_feats + num_feat}], TYPE={type}, POSSPER={possessor_person}, POSSNUM={possessor_num}] -> '{word}'\n")
