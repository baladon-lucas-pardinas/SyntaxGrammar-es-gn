import argparse

def read_trees_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        trees = []
        tree = ""

        stack = []
        counter = 0

        for char in content:
            if char == '(':
                if counter == 0:
                    tree = ""
                counter += 1
                stack.append(char)
            elif char == ')':
                counter -= 1
                stack.pop()
                if counter == 0:
                    tree += char
                    trees.append(tree)
            if counter > 0:
                tree += char

        return trees


def divide_and_save_files(trees, n, output_prefix):
    num_trees = len(trees)
    trees_per_file = num_trees // n
    remainder = num_trees % n

    start_idx = 0
    for i in range(n):
        end_idx = start_idx + trees_per_file + (1 if i < remainder else 0)
        output_filename = f"{output_prefix}{i + 1}.txt"

        with open(output_filename, 'w') as output_file:
            output_file.write('\n'.join(trees[start_idx:end_idx]) + '\n')

        start_idx = end_idx


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Divide tree file into multiple smaller files.")
    parser.add_argument("input_file", type=str, help="Path to the input file containing tree structures")
    parser.add_argument("num_files", type=int, help="Number of output files to create")
    parser.add_argument("output_prefix", type=str, help="Prefix for the output file names")

    args = parser.parse_args()

    input_filename = args.input_file
    num_files = args.num_files
    output_prefix = args.output_prefix

    trees = read_trees_from_file(input_filename)
    divide_and_save_files(trees, num_files, output_prefix)
