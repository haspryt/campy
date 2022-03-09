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
    
def loop_check(file_name: str):

    cpc_file = open(file_name, 'r')
    cpc_lines = cpc_file.readlines()

    exp_if_indent = 0
    exp_while_indent = 0
    exp_repeat_indent = 0
    exp_for_indent = 0
    exp_indent = 0
    current_line = 0

    for line in cpc_lines:
        current_line += 1
        if (line.strip() == ''):
            continue
        if exp_indent > 0:
            indent_str = "    " * exp_indent
        else:
            indent_str = ''

        if exp_indent > 1:
            indent_str_prev = "    " * (exp_indent - 1)
        else:
            indent_str_prev = ''

        if line.startswith(indent_str):
            l = len(indent_str)
            if line[l] == ' ':
                raise Exception("Unexpected indent, line: " + str(current_line))
            line_split = line.split("//", 1)
            line_stripped = line_split[0].strip()
            if line_stripped.startswith("ENDIF") or line_stripped.startswith("ENDWHILE") or line_stripped.startswith("UNTIL") or line_stripped.startswith("NEXT"):
                raise Exception("Unexpected indent, line: " + str(current_line))
            elif line_stripped.startswith("IF"):
                exp_if_indent += 1
                if line_stripped[-4:] != "THEN":
                    raise Exception("Expected THEN at end of IF clause, line: " + str(line))
            elif line_stripped.startswith("WHILE"):
                exp_while_indent += 1
            elif line_stripped.startswith("REPEAT"):
                exp_repeat_indent += 1
            elif line_stripped.startswith("FOR"):
                exp_for_indent += 1
            
        elif line.startswith(indent_str_prev):
            line_stripped = line.strip()
            if line_stripped.startswith("ENDIF"):
                if exp_if_indent > 0:
                    exp_if_indent -= 1
                else:
                    raise Exception("Unexpected ENDIF, line: " + str(current_line))
            
            elif line_stripped.startswith("ELSE"):
                pass
            
            elif line_stripped.startswith("ENDWHILE"):
                if exp_while_indent > 0:
                    exp_while_indent -= 1
                else:
                    raise Exception("Unexpected ENDWHILE, line: " + str(current_line))

            elif line_stripped.startswith("UNTIL"):
                if exp_repeat_indent > 0:
                    exp_repeat_indent -= 1
                else:
                    raise Exception("Unexpected UNTIL, line: " + str(current_line))
            
            elif line_stripped.startswith("NEXT"):
                if exp_for_indent > 0:
                    exp_for_indent -= 1
                else:
                    raise Exception("Unexpected NEXT, line: " + str(current_line))
            else:
                raise Exception("Missing indent, line: " + str(current_line))
        else:
            raise Exception("Missing indent, line: " + str(current_line))

        exp_indent = exp_if_indent + exp_for_indent + exp_while_indent + exp_repeat_indent
        