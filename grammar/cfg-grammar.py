### This code removes all features from the feature grammar, leaving behind a context-free grammar
import argparse

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
    return parser.parse_args()

def main():
    args = parse_args()
    process_featgram(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
