### Read: https://www.nltk.org/book/ch09.html
import csv


def write_adjective_productions(grammar_file, noun_lexicon):
    # Load noun lexical rules from CSV
    with open(noun_lexicon, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            shifted_row = [row[1]] + row[-9:]
            word = shifted_row[1]
            gender = shifted_row[6]
            number = shifted_row[7]

            num_feats = [f"NUM={number.lower()}"]
            if (number == "N"):
                num_feats = [f"NUM={num.lower()}" for num in ["S", "P"]]

            gender_feat = f", GEN={gender.lower()}" if gender != "C" else ""
            
            for num_feat in num_feats:
                grammar_file.write(f"A[AGR=[{num_feat + gender_feat}]] -> '{word}'\n")
