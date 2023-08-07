from ..parsing.parse_labels import parse_labels
from ..parsing.parse_tree import parse_tree
import codecs


def fetch_spanish_trees(filepath):
    with codecs.open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

        trees = []
        tree_start = -1
        stack = []

        for i, char in enumerate(content):
            if char == '(':
                if not stack:
                    tree_start = i
                stack.append('(')
            elif char == ')':
                if len(stack) == 1:
                    trees.append(content[tree_start:i+1])
                stack.pop()

    parsed_trees = [parse_tree(x) for x in trees]
    for tree in parsed_trees:
        parse_labels(tree)
    return parsed_trees