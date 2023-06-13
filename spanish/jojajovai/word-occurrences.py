import csv

# Load the parallel corpus data
corpus_file = 'jojajovai_all.csv'
corpus_data = []
with open(corpus_file, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        if row[0] == 'train':
            corpus_data.append(row[5])

# List of word_data files
word_files = ['../spanish-verbs/matched-verbs.csv',
              '../spanish-nouns/matched-nouns.csv',
              '../spanish-adjectives/matched-adjectives.csv']

# Create a dictionary to store word occurrences
word_occurrences = {}

# Initialize the dictionary with word categories, base forms, and counts
for word_file in word_files:
    with open(word_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            word = row[1]
            base_form = row[2]
            category = row[3]
            
            if category not in word_occurrences:
                word_occurrences[category] = {}
            
            word_occurrences[category][word] = (base_form, 0)

# Count word occurrences in the train set
for sentence in corpus_data:
    words = sentence.split()
    for word in words:
        for category in word_occurrences:
            if word in word_occurrences[category]:
                base_form, count = word_occurrences[category][word]
                count += 1
                word_occurrences[category][word] = (base_form, count)

# Build a dictionary with word categories and base forms
# and their respective total occurrences in the train set
base_form_occurrences = {}
for category in word_occurrences:
    for word, (base_form, count) in word_occurrences[category].items():
        if base_form not in base_form_occurrences:
            base_form_occurrences[base_form] = 0
        base_form_occurrences[base_form] += count

# Write the output to a CSV file
output_file = 'word_occurrences.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Word Category', 'Word', 'Occurrences', 'Base Form', 'Total Occurrences'])
    for category in word_occurrences:
        for word, (base_form, count) in word_occurrences[category].items():
            total_occurrences = base_form_occurrences[base_form]
            writer.writerow([category, word, count, base_form, total_occurrences])

print("Word occurrences counted and saved in", output_file)
