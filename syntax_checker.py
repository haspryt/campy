import string

def syntax_check(file_name: str):
    
    cpc_file = open(file_name, 'r')
    cpc_lines = cpc_file.readlines()

    valid_chars = list(string.ascii_lowercase) + list(string.ascii_uppercase) + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '?', '!', '.', '@', '^', '~', '`', '\'', '_', '|', '/', '#', '$', '&', '%', '{', '}', '+', '*', ':', ';', ',', '>', '<', '=', '(', ')', '[', ']', '-', ' ', '\"']
    current_line = 1
    

    for line in cpc_lines:
        for char in range(len(line) - 1):
            if line[char] not in valid_chars:
                print(line[char])
                raise Exception("Invalid character, line: " + str(current_line))
        current_line += 1