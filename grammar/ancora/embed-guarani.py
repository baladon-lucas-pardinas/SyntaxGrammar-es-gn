import argparse
import csv
import re
import string

def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def read_sentences_from_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        return [row[0] for row in csv_reader]
    
def read_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        return [row for row in csv_reader]

def build_indices_dict(indices_file: str) -> dict[int, list[tuple[int, int, int]]]:
    indices_dict = {}
    with open(indices_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row_index, row in enumerate(csv_reader):
            sentence_index = int(row[0])
            start_index = int(row[1])
            end_index = int(row[2])
            indices_dict.setdefault(sentence_index, []).append((row_index, start_index, end_index))
    return indices_dict

def embed_guarani(sentence: str, indices: list[tuple[int, int, int]], translations: list[str]) -> str:
    modified_segments = []  # List to store the segments of the modified sentence
    current_position = 0  # Keep track of the current position in the sentence

    for index in indices:
        row_index, start_index, end_index = index
        translation = translations[row_index]

        # Append the portion of the sentence before the replacement
        modified_segments.append(sentence[current_position:start_index])

        # Append the translation
        modified_segments.append(translation)

        # Update the current position to the end of the replaced portion
        current_position = end_index

    # Append the remaining portion of the sentence
    modified_segments.append(sentence[current_position:])

    # Join the segments to create the modified sentence
    modified_sentence = ''.join(modified_segments)
    
    return modified_sentence

def preprocess_guarani(sentence: str) -> str:
    pass # Placeholder, should preprocess * stuff

def postprocess_pair(pair: list[str]) -> list[str]:
    
    def postprocess_guarani(sentence: str) -> str:
        pass # Placeholder, should postprocess _pe and other stuff

    def join_punctuation(line : str):
        punctuations = string.punctuation
        for punctuation in punctuations:
            line = line.replace(f" {punctuation}", punctuation)
        for punctuation in "¿¡":
            line = line.replace(f"{punctuation} ", punctuation)
        return re.sub(r'\s+', ' ', line).strip()

    def undo_contractions(line : str):
        return line.replace(" al ", " a el ").replace(" del ", " de el ")
    
    pair[1] = postprocess_guarani(pair[1])

    # Apply this postprocess to both guarani and spanish sentences
    return [join_punctuation(undo_contractions(sent)) for sent in pair]

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process sentences and embed Guarani translations')
    parser.add_argument('--indices', required=True, help='Path to the indices CSV file')
    parser.add_argument('--extracted', required=True, help='Path to the extracted CSV file')
    parser.add_argument('--translations', required=True, help='Path to the translations CSV file')
    parser.add_argument('--output', required=True, help='Path to the output CSV file')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Build indices dictionary
    indices_dict = build_indices_dict(args.indices)

    # Read translations
    translations = [row[1] for row in read_csv(args.translations)]

    # Preprocess translations
    translations = [preprocess_guarani(translation) for translation in translations]

    # Process each sentence and embed Guarani translations, obtaining bilingual pairs
    bilingual_pairs  = []
    extracted_sentences = read_sentences_from_csv(args.extracted)
    for sentence_index, extracted_sentence in enumerate(extracted_sentences):
        indices = indices_dict.get(sentence_index, [])  # Get the indices for this sentence index
        if indices:
            embedded_sentence = embed_guarani(extracted_sentence, indices, translations)
            bilingual_pairs.append([extracted_sentence, embedded_sentence])

    # Post-process the resulting sentence pairs
    bilingual_pairs = [postprocess_pair(pair) for pair in bilingual_pairs]

    # Write bilingual pairs to output CSV file
    with open(args.output, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(bilingual_pairs)


if __name__ == '__main__':
    main()
