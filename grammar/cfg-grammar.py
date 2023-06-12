### This code removes all features from the feature grammar, leaving behind a context-free grammar
import argparse
import csv

def get_word_weights(filepath):
    result = {}
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            category = row[0]
            word = row[1]
            occurrences = int(row[2])
            base_form = row[3]
            total_occurrences = int(row[4])

            if category not in result:
                result[category] = ({}, {})
            
            (word_data, base_form_data) = result[category]

            word_data[word] = (occurrences, base_form, total_occurrences)
            if base_form not in base_form_data:
                base_form_data[base_form] = total_occurrences

    return result

def isRule(line: str):
    return (not not line) and not line.startswith("#") and not line.startswith("%")

def add_weights(filepath, word_weights):
    lines = []  # Store the lines of the file

    with open(filepath, 'r') as file:
        for line in file:
            if isRule(line):
                lhs, rhs = line.split("->")
                lhs = lhs.strip()
                if lhs in word_weights:
                    (word_data, _) = word_weights[lhs]
                    rhs = rhs.replace("'", "").replace('"', '').strip()
                    base_form_occurrences = word_data[rhs][2]
                    line = f"{line.rstrip()} # {base_form_occurrences}\n"
                else:
                    line = f"{line.rstrip()} # \n"
            lines.append(line)  # Store the line in the list

    # Write the updated content back to the file
    with open(filepath, 'w') as file:
        file.writelines(lines)


def process_featgram(input_file, output_file):
    with open(input_file, 'r') as input_file, open(output_file, 'w') as output_file:
        for line in input_file:
            new_line = ''
            stack = []
            for char in line:
                if char == '[':
                    stack.append('[')
                elif char == ']':
                    stack.pop()
                elif not stack:
                    new_line += char
            output_file.write(new_line)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Path to the input featgram file')
    parser.add_argument('output_file', help='Path to the output cfg file')
    parser.add_argument('-w', '--word-weights', help='Path to the word weights file')
    return parser.parse_args()

def main():
    args = parse_args()
    process_featgram(args.input_file, args.output_file)
    if args.word_weights:
        word_weights = get_word_weights(args.word_weights)
        add_weights(args.output_file, word_weights)
        

if __name__ == '__main__':
    main()
