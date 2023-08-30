import csv
import sys
import string
import re

# Read input file and extract lines starting with "# text = "
def extract_lines(input_filename):
    lines_to_save = []
    with open(input_filename, 'r') as file:
        for line in file:
            if line.startswith("# text = "):
                lines_to_save.append(line[len("# text = "):].strip())
    return lines_to_save

def separate_punctuation(line : str):
    punctuations = string.punctuation + "¿¡"
    for punctuation in punctuations:
        if (punctuation == '.'):
            # Replace periods with a space on both sides only if the period is not between two numbers
            line = re.sub(r'(?<!\d)\.(?!\d)', ' . ', line)
        elif (punctuation == ','):
            # Replace commas with a space on both sides only if the comma is not between two numbers
            line = re.sub(r'(?<!\d)\,(?!\d)', ' , ', line)
        else:
            line = line.replace(punctuation, f" {punctuation} ")
    return re.sub(r'\s+', ' ', line).strip()

def undo_contractions(line : str):
    return line.replace(" al ", " a el ").replace(" del ", " de el ")

def process_lines(lines : list[str]):
    processed_lines = []
    for line in lines:
        line = line.lower()
        line = separate_punctuation(line)
        line = undo_contractions(line)
        processed_lines.append(line)
    return processed_lines

# Save extracted lines to a CSV file
def save_to_csv(lines, output_filename):
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            writer.writerow([line])

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py input_filename output_filename")
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    extracted_lines = extract_lines(input_filename)
    processed_lines = process_lines(extracted_lines)
    save_to_csv(processed_lines, output_filename)
    print(f"Extracted {len(processed_lines)} lines and saved to {output_filename}.")

if __name__ == "__main__":
    main()
