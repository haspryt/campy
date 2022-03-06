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
            return all_tokens[index]


def form_tree(all_tokens: list, operators: list):
    
    #get_user_def_operators(all_tokens, operators)
    tree = ()
    for (index, token) in enumerate(all_tokens):
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
                case '+'| '-' | '*' | '/' | '>' | '<' | '=' | '<>' | '<=' | '>=' | '<-' | '&' | "AND" | "NOT" | "OR":
                    args = (get_arg(index - 1, all_tokens, operators), get_arg(index + 1, all_tokens, operators))
                    tree += ((token, args),)
                
                case "OUTPUT" | "DECLARE":
                    arg = get_arg(index + 1, all_tokens, operators)
                    #print(arg)
                    #print(index)
                    tree += ((token, arg),)

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

                case "ELSE":
                    saved_index = index
                    current = token
                    while current != "ENDIF":                        
                        current = all_tokens[index]
                        index += 1
                    block = form_tree(all_tokens[slice(saved_index + 1, index)], operators)
                    tree += ((token, block),)
    return tree