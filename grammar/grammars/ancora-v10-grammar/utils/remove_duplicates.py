def remove_duplicates(file_path):
    lines_seen = set()  # Set to store unique lines
    updated_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if line not in lines_seen:
                lines_seen.add(line)
                updated_lines.append(line)
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

# # Example usage
# file_path = 'data.txt'
# remove_duplicates_in_place(file_path)
