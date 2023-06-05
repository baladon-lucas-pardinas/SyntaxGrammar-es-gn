Beware of the fact that "Usted" and "Ustedes" are changed into 3rd person in their AGR.

python third-grammar/create-featgram.py ../../spanish/spanish-verbs/matched-verbs.csv ../../spanish/spanish-nouns/matched-nouns.csv ../../spanish/transitivity-scraping/transitivities.csv -d ../../spanish/spanish-determiners/determiners.csv -o ../grammar-files/g3/feature-grammar.txt

python fourth-grammar/create-featgram.py ../../spanish/spanish-verbs/matched-verbs.csv ../../spanish/spanish-nouns/matched-nouns.csv ../../spanish/transitivity-scraping/transitivities.csv -d ../../spanish/spanish-determiners/determiners.csv -p ../../spanish/spanish-pronouns/pronouns.csv -o ../grammar-files/g4/feature-grammar.txt