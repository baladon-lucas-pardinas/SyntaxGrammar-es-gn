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

    punctuations = ''.join([char for char in punctuations if char not in '"\'.,'])

    opening_quote = "QUOTE_OPEN"
    closing_quote = "QUOTE_CLOSE"
    single_opening_quote = "SINGLE_QUOTE_OPEN"
    single_closing_quote = "SINGLE_QUOTE_CLOSE"

    # Add spaces to the side of punctuations
    for punctuation in punctuations:
        line = line.replace(punctuation, f" {punctuation} ")

    # Replace periods with a space on both sides only if the period is not between two numbers
    line = re.sub(r'(?<!\d)\.(?!\d)', ' . ', line)
    # Replace commas with a space on both sides only if the comma is not between two numbers
    line = re.sub(r'(?<!\d)\,(?!\d)', ' , ', line)

    # Small hack for dealing with quotation marks at beginning or end of string
    if line.startswith('"') or line.startswith("'"):
        line = " " + line
    if line.endswith('"') or line.endswith("'"):
        line = line + " "
    
    # Replace double quotes with a space on both sides and tag them as OPEN or CLOSE
    line = line.replace(' "', f" {opening_quote} ").replace('" ', f" {closing_quote} ")

    # Replace single quotes with a space on both sides and tag them as OPEN or CLOSE
    line = line.replace(" '", f" {single_opening_quote} ").replace("' ", f" {single_closing_quote} ")

    return re.sub(r'\s+', ' ', line).strip()

def undo_contractions(line : str):
    return line.replace(" al ", " a el ").replace(" del ", " de el ")

def process_lines(lines : list[str]):
    processed_lines = []
    i = 0
    for line in lines:
        if (len(line) > 3 ): # Otherwise some lines are empty or just a period, etc
            i += 1
            if line[0] not in string.punctuation + "¿¡":
                line = line[0].lower() + line[1:]
            elif line[1] not in string.punctuation + "¿¡":
                line = line[0] + line[1].lower() + line[2:]
            else:
                line = line[0] + line[1] + line[2].lower() + line[3:]
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
