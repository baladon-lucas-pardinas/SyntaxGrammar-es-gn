def rule_to_cfg(line: str):
    new_line = ''
    stack = []
    for char in line:
        if char == '[':
            stack.append('[')
        elif char == ']':
            stack.pop()
        elif not stack:
            new_line += char
    return new_line