def replace_variables(first_dict, second_dict):
    for key, value in second_dict.items():
        if isinstance(value, dict):
            replace_variables(first_dict, value)  # Recursively search nested dictionaries
        elif value in first_dict:
            second_dict[key] = first_dict[value]  # Replace matching value with corresponding value from the first dictionary

# # Example usage
# first_dict = {
#     '?a': 'somevalue',
#     '?b': 'someOtherValue',
# }

# second_dict = {
#     'AGR': {
#         'PER': 1,
#         'NUM': 'pl',
#         'TENSE': '?b',
#     },
#     'MOOD': '?a',
#     'TRANS': 'intr',
# }

# replace_values(first_dict, second_dict)
# print(second_dict)
