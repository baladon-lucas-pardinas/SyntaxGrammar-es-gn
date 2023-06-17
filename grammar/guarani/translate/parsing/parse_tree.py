def parse_tree(tree_str):
    stack = []
    current_node = None
    principio = False
    termino = False

    for char in tree_str:
        if char == "(":
            if current_node is not None:
                stack.append(current_node)
            current_node = {'type': '', 'label': '', 'children': [], 'word': ''}
            principio = True
            termino = False
        elif char == ")":
            if stack:
                parent_node = stack.pop()
                parent_node['children'].append(current_node)
                current_node = parent_node
                termino = False
        elif char == "[":
            termino = False
            principio = False
            current_node['label'] += char  # Include the square bracket in the label
        elif char == "]":
            termino = True
            current_node['label'] += char  # Include the square bracket in the label
        else:
            if principio and not str.isspace(char):
                current_node['type'] += char
            elif termino and not str.isspace(char):
                if char == ',':
                    current_node['label'] += char
                    termino = False
                else:
                    current_node['word'] += char
            elif not str.isspace(char):
                current_node['label'] += char

    return current_node