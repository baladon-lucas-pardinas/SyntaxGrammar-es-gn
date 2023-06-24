import re

def parse_rule(rule_string):
    rule_parts = re.findall(r'(\w+)\[([\w=,?]+)\]', rule_string)
    conditions = {}

    for part in rule_parts:
        symbol, condition = part
        condition_dict = {}

        for item in condition.split(','):
            key, value = item.split('=')
            condition_dict[key.strip()] = value.strip()

        if symbol not in conditions:
            conditions[symbol] = condition_dict
        else:
            conditions[symbol].update(condition_dict)

    item_conditions = {}
    symbol_indices = {}
    index_counter = 0

    for symbol in conditions.keys():
        symbol_indices[symbol] = index_counter
        index_counter += 1

    for symbol, condition_dict in conditions.items():
        for key, value in condition_dict.items():
            if key not in item_conditions:
                item_conditions[key] = {}

            if value not in item_conditions[key]:
                item_conditions[key][value] = []

            item_conditions[key][value].append(symbol_indices[symbol])

    return item_conditions

# # Example usage:
# rule_string = "D[AGR=?a, NAS=?n] N[AGR=?a, NAS=?n] V[AGR=?a]"
# parsed_rule = parse_rule(rule_string)
# print(parsed_rule)
