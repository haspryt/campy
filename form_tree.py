#guide_tokens = ["ENDIF", "ENDCASE", "ENDWHILE", "ENDPROCEDURE", "ENDFUNCTION", "ENDTYPE", "ENDCLASS", "THEN", "TO", "OF"]

def get_user_def_operators(all_tokens: list, operators: list):
    for token in all_tokens:
        if token == "FUNCTION" or token == "PROCEDURE":
            operators.append(all_tokens[token + 1])

def get_arg(index: int, all_tokens: list, operators: list):
    match all_tokens[index]:
        case '(':
            saved_index = index
            p_counter = 1
            while p_counter > 0:
                index += 1
                match all_tokens[index]:
                    case '(':
                        p_counter += 1
                    case ')':
                        p_counter -= 1
            return form_tree(all_tokens[slice(saved_index + 1, index)], operators)
        case ')':
            saved_index = index
            p_counter = 1
            while p_counter > 0:
                index += 1
                match all_tokens[index]:
                    case ')':
                        p_counter += 1
                    case '(':
                        p_counter -= 1
            return form_tree(all_tokens[slice(index + 1, saved_index)], operators)
        case _:
            if all_tokens[index] == "INPUT":
                all_tokens[index] = "input('')"
            return all_tokens[index]


def form_tree(all_tokens: list, operators: list):
    tree = ()
    real_index = 0
    while True:
        index = real_index
        try:
            token = all_tokens[real_index]
        except:
            break
        p_counter = 0
        if index == 0 and token == '(':
            p_counter -= 1
        match token:
            case '(':
                p_counter += 1
            case ')':
                p_counter -= 1

        if token in operators and p_counter == 0:
            match token:
                case '+'| '-' | '*' | '/' | '>' | '<' | '=' | '<>' | '<=' | '>=' | '&' | "AND" | "NOT" | "OR" | "DIV" | "MOD":
                    args = (get_arg(index - 1, all_tokens, operators), get_arg(index + 1, all_tokens, operators))
                    tree += ((token, args),)

                case '<-':
                    if all_tokens[index - 2] != "FOR":
                        args = (get_arg(index - 1, all_tokens, operators), get_arg(index + 1, all_tokens, operators))
                        tree += ((token, args),)
                
                #case "INPUT":
                #    arg = get_arg(index + 1, all_tokens, operators)
                #    tree += (('<-', (arg, "input()")),)

                case "OPENFILE":
                    ident = all_tokens[index + 1]
                    mode = all_tokens[index + 3]
                    tree += ((token, (ident, mode)),)
                    real_index += 3

                case "DECLARE" | "PUBLIC" | "PRIVATE":
                    arg = get_arg(index + 1, all_tokens, operators)
                    v_type = get_arg(index + 3, all_tokens, operators)
                    tree += ((token, (arg, v_type)),)
                    real_index += 3

                case "IF":
                    saved_index = index
                    current = token

                    while current != "THEN":
                        current = all_tokens[index]
                        index += 1
                    condition = form_tree(all_tokens[slice(saved_index + 1, index)], operators)

                    saved_index = index
                    if_counter = 1
                    while (current != "ENDIF" or current != "ELSE") and if_counter >= 1:
                        current = all_tokens[index]
                        index += 1
                        if current == "IF":
                            if_counter += 1
                        elif current == "ENDIF":
                            if_counter -= 1
                    
                    block = form_tree(all_tokens[slice(saved_index + 1, index)], operators)
                    tree += ((token, (condition, block)),)
                    real_index = index

                case "ELSE":
                    saved_index = index
                    current = token
                    while current != "ENDIF":                        
                        current = all_tokens[index]
                        index += 1
                    block = form_tree(all_tokens[slice(saved_index + 1, index)], operators)
                    tree += ((token, block),)
                    real_index = index
                
                case "FOR":
                    if all_tokens[index - 2] != "OPENFILE":
                        ident = all_tokens[index + 1]
                        init = all_tokens[index + 3]
                        end = all_tokens[index + 5]
                        step = 1
                        if all_tokens[index + 6] == "STEP":
                            step = all_tokens[index + 7]
                        while current != "NEXT":
                            current = all_tokens[index]
                            index += 1
                        block = form_tree(all_tokens[slice(saved_index + 1, index)], operators)
                        tree += ((token, (ident, init, end, step)),)
                        real_index = index
                
                case "WHILE":
                    saved_index = index
                    current = token

                    while current != "\n":
                        current = all_tokens[index]
                        index += 1
                    condition = form_tree(all_tokens[slice(saved_index + 1, index)], operators)

                    saved_index = index
                    current = token

                    while current != "ENDWHILE":                        
                        current = all_tokens[index]
                        index += 1
                    block = form_tree(all_tokens[slice(saved_index + 1, index)], operators)
                    tree += ((token, (condition, block)),)
                    real_index += index

                case "REPEAT":
                    saved_index = index
                    current = token

                    while current != "UNTIL":                        
                        current = all_tokens[index]
                        index += 1
                    block = form_tree(all_tokens[slice(saved_index + 1, index)], operators)

                    saved_index = index
                    current = token

                    while current != "\n":
                        current = all_tokens[index]
                        index += 1
                    condition = form_tree(all_tokens[slice(saved_index + 1, index)], operators)

                    tree += (block, ("WHILE", (condition, block))) # Hacky but works
                    real_index = index

                case "OUTPUT" | "CALL" | "RETURN" | "EOF" | "CLOSEFILE" | _:
                    arg = get_arg(index + 1, all_tokens, operators)
                    tree += ((token, arg),)

        real_index += 1
                    
    return tree