### This code removes all features from the feature grammar, leaving behind a context-free grammar

with open('./feature-grammar.txt', 'r') as input_file, open('./cfg-grammar.txt', 'w') as output_file:
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
