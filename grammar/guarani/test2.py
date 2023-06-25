import re

def parse_string(input_string):
    result_dict = {}

    # Find all occurrences of [KEY='VALUE']
    matches = re.findall(r'\[(.*?)\]', input_string)

    for index, match in enumerate(matches):
        # Split the key-value pairs
        pairs = match.split(', ')

        for pair in pairs:
            key, value = pair.split('=')

            # Remove the surrounding single quotes from the value
            value = value.strip("'")

            if value.startswith('?'):
                if key in result_dict:
                    if value in result_dict[key]:
                        result_dict[key][value].append(index)
                    else:
                        result_dict[key][value] = [index]
                else:
                    result_dict[key] = {value: [index]}

    return result_dict

# if main run the previous function
if (__name__ == "__main__"):
    print(parse_string("D[AGR='?a', NAS='?n'] N[AGR='?a', NAS='?n'] V[AGR='?a']"))
    print(parse_string("D[AGR='?a', NAS='?n', TER='a'] N[AGR='?a', NAS='?n', COMP=2] V[AGR='?a', COMP=2]"))
    