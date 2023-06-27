def extract_words(data):
    result = ''
    if 'word' in data and data['word']:
        result += data['word'] + ' '
    if 'children' in data:
        for child in data['children']:
            result += extract_words(child)
    return result