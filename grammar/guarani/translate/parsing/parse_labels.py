import ast

# Example label: "[AGR=[NUM='p',PER=3,TENSE='i'],MOOD='i',SUBCAT='intr']"
def parse_label(label : str):
    
    label = label.replace(' ', '')

    # Turn into a JSON-like string
    label = label.replace('[', '{').replace(']', '}').replace('=', ':')

    # Add quotes around JSON labels
    label = label.replace(':', '":').replace(',', ',"').replace('{', '{"')

    # Parse the modified JSON string using ast.literal_eval()
    json_dict = ast.literal_eval(label)

    return json_dict

# Perform the above function recursively on a tree
def parse_labels(tree: dict):
    if 'label' in tree:
        tree['label'] = parse_label(tree['label'])
    if 'children' in tree:
        for child in tree['children']:
            parse_labels(child)