import re

def parse_rule(input_string):
    # print(input_string)
    result_dict = {}

    # Find all occurrences of [KEY='VALUE']
    matches = re.findall(r'\[(.*?)\]', input_string)
    # print(matches)

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

# # Example usage:
# rule_string = "D[AGR=?a, NAS=?n] N[AGR=?a, NAS=?n] V[AGR=?a]"
# parsed_rule = parse_rule(rule_string)
# print(parsed_rule)
