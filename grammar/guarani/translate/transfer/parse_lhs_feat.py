from translate.parsing.parse_labels import parse_label

def get_string_from_bracket(text: str):
    if "[" not in text:
        return None
    
    start_index = text.index("[")
    substring = text[start_index:]
    return substring

def parse_lhs_features(lhs: str):
    label = get_string_from_bracket(lhs)
    if label == None:
        return {}
    print(label)
    return parse_label(label)