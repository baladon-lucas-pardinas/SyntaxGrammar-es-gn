import csv


def write_adverb_productions(grammar_file, adverb_lexicon):
    with open(adverb_lexicon, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            grammar_file.write(f"R -> '{row[1]}'\n")
