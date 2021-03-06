from destructure_tree import destructure_tree

#guide_tokens = ["ENDIF", "ENDCASE", "ENDWHILE", "ENDPROCEDURE", "ENDFUNCTION", "ENDTYPE", "ENDCLASS", "THEN", "TO", "OF"]

def get_user_def_operators(all_tokens: list, operators: list):
    for (i, token) in enumerate(all_tokens):
        if token == "FUNCTION" or token == "PROCEDURE":
            operators.append(all_tokens[i + 1])

def chain(all_tokens: list, operators: list):
    if len(all_tokens) == 1:
        return all_tokens[0]

    chainable = ['+', '-', '*', '/', 'MOD', 'DIV', '&', ',']
    left = get_arg(0, all_tokens, operators)
    #print("!!" + str(left))
    p_counter = 0
    for (index, token) in enumerate(all_tokens):
        match token:
            case '(':
                p_counter += 1
            case ')':
                p_counter -= 1
        if (token in chainable) and (p_counter == 0):
            if token == ',':
                token = '&'
            return ((token, (left, chain(all_tokens[index + 1:], operators))),)
    return all_tokens[0]

def get_fn_args(tokens_slice: list):
    to_return = ()
    for i in range(0, len(tokens_slice), 3):
        ident = tokens_slice[i]
        current_type = tokens_slice[i + 2]
        to_return += ((ident, current_type),)
    return to_return

def get_arg(index: int, all_tokens: list, operators: list):
    p_counter = 0
    if all_tokens[index] in operators:
        saved_index = index
        index += 1
        match all_tokens[index]:
            case '(':
                p_counter += 1
            case ')':
                p_counter -= 1
        index += 1
        while p_counter > 0:
            match all_tokens[index]:
                case '(':
                    p_counter += 1
                case ')':
                    p_counter -= 1
            index += 1
        return form_tree(all_tokens[saved_index : index], operators)
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
            return form_tree(all_tokens[saved_index + 1 : index], operators)
        case ')':
            saved_index = index
            p_counter = 1
            while p_counter > 0:
                index -= 1
                match all_tokens[index]:
                    case ')':
                        p_counter += 1
                    case '(':
                        p_counter -= 1
            if not all_tokens[index - 1] in operators:
                return form_tree(all_tokens[index + 1 : saved_index], operators)
            else:
                return form_tree(all_tokens[index : saved_index], operators)
        case _:
            if all_tokens[index] == "INPUT":
                all_tokens[index] = "input('')"
            return all_tokens[index]


def form_tree(all_tokens: list, operators: list):
    tree = ()
    real_index = 0
    #if all_tokens[0] == '(':
    #    p_counter = -1
    #else:
    p_counter = 0
    while True:
        index = real_index
        try:
            token = all_tokens[real_index]
        except:
            break
        match token:
            case '(':
                p_counter += 1
            case ')':
                p_counter -= 1

        if token in operators and p_counter == 0:
            match token:
                case '+'| '-' | '*' | '/' | ',' | '&' | "DIV" | "MOD":
                    saved_index = index
                    index += 1
                    while not token in ['>', '<', '==', '!=', '<>', '>=', '<=', 'AND', 'NOT', 'OR', '\n']:
                        try:
                            token = all_tokens[index]
                        except:
                            #index -= 1
                            break
                        index += 1
                    p_c = 0
                    if all_tokens[saved_index - 1] == ')':
                        p_c += 1
                    while p_c > 0:
                        saved_index -= 1
                        current = all_tokens[saved_index]
                        if current == '(':
                            p_c -= 1
                        elif current == ')':
                            p_c += 1
                    #if not all_tokens[saved_index] in ['IF', 'WHILE', 'UNTIL']:
                    out = chain(all_tokens[saved_index - 1 : index], operators)
                    #else:
                    #    out = chain(all_tokens[saved_index : index], operators)
                    real_index = index 
                    #print(out)
                    tree += out
                
                case  '>' | '<' | '=' | '<>' | '<=' | '>=' | "AND" | "NOT" | "OR":
                    args = (get_arg(index - 1, all_tokens, operators), get_arg(index + 1, all_tokens, operators))
                    #print("!" + str(args))
                    tree += ((token, args),)

                case '<-':
                    if all_tokens[index - 2] != "FOR":
                        #args = (get_arg(index - 1, all_tokens, operators), get_arg(index + 1, all_tokens, operators))
                        until = index
                        while token != "\n":
                            until += 1
                            try:
                                token = all_tokens[until]
                            except:
                                break
                        args = (all_tokens[index - 1], chain(all_tokens[index + 1 : until], operators))
                        tree += ((all_tokens[index], args),)
                        real_index = until

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
                    condition = form_tree(all_tokens[saved_index + 1 : index], operators)

                    saved_index = index
                    if_counter = 1
                    while (current != "ENDIF" or current != "ELSE") and if_counter >= 1:
                        current = all_tokens[index]
                        index += 1
                        if current == "IF":
                            if_counter += 1
                        elif current == "ENDIF":
                            if_counter -= 1
                    
                    block = form_tree(all_tokens[saved_index + 1 : index], operators)
                    tree += ((token, (condition, block)),)
                    real_index = index

                case "ELSE":
                    saved_index = index
                    current = token
                    while current != "ENDIF":                        
                        current = all_tokens[index]
                        index += 1
                    block = form_tree(all_tokens[saved_index + 1 : index], operators)
                    tree += ((token, block),)
                    real_index = index
                
                case "FOR":
                    if all_tokens[index - 2] != "OPENFILE":
                        saved_index = index
                        ident = all_tokens[index + 1]
                        init = all_tokens[index + 3]
                        end = all_tokens[index + 5]
                        step = '1'
                        to_add = 6
                        if all_tokens[index + 6] == "STEP":
                            step = all_tokens[index + 7]
                            to_add = 8
                        while token != "NEXT":
                            token = all_tokens[index]
                            index += 1
                        block = form_tree(all_tokens[saved_index + to_add : index], operators)
                        tree += (("FOR", ((ident, init, end, step), block)),)
                        real_index = index
                
                case "WHILE":
                    saved_index = index
                    current = token

                    while current != "\n":
                        current = all_tokens[index]
                        index += 1
                    condition = form_tree(all_tokens[saved_index + 1 : index], operators)

                    saved_index = index
                    current = token

                    while current != "ENDWHILE":                        
                        current = all_tokens[index]
                        index += 1
                    block = form_tree(all_tokens[saved_index : index], operators)
                    tree += ((token, (condition, block)),)
                    real_index = index

                case "REPEAT":
                    saved_index = index
                    current = token

                    while current != "UNTIL":
                        current = all_tokens[index]
                        index += 1
                    block = form_tree(all_tokens[saved_index + 1 : index - 1], operators)

                    saved_index = index
                    #current = token

                    while current != "\n":
                        try:
                            current = all_tokens[index]
                        except:
                            break
                        index += 1
                    condition = form_tree(all_tokens[saved_index : index], operators)
                    #print("!")
                    #print(all_tokens[saved_index : index])
                    #print(condition)
                    tree += block
                    tree += (("WHILE", (condition, block)),) # Hacky but hey
                    real_index = index

                case "OUTPUT":
                    saved_index = index
                    t = token
                    while t != '\n':
                        index += 1
                        try:
                            t = all_tokens[index]
                        except:
                            break
                    #print(all_tokens[saved_index + 1 : index])
                    arg = form_tree(all_tokens[saved_index + 1 : index], operators)
                    try:
                        temp = arg[0]
                        exists = True
                    except:
                        exists = False
                    if not exists:
                        arg = (get_arg(saved_index + 1, all_tokens, operators),)
                    #real_arg = ()
                    #for a in arg:
                    #    real_arg += (('str(' + a + ')'),)
                    tree += ((token, arg),)
                    real_index = index

                #case '&':
                #    pass

                case "PROCEDURE" | "FUNCTION":
                    saved_index = index
                    ident = all_tokens[index + 1]
                    while token != '\n':
                        index += 1
                        token = all_tokens[index]
                    newline_index = index
                    offset = 1
                    ret_type = "NONE"
                    if all_tokens[saved_index] == "FUNCTION":
                        offset += 2
                        ret_type = all_tokens[index - 1]
                    fn_args = get_fn_args(all_tokens[saved_index + 3 : newline_index - offset])
                    while token != "ENDPROCEDURE" and token != "ENDFUNCTION":
                        index += 1
                        token = all_tokens[index]
                    block = form_tree(all_tokens[newline_index : index], operators)
                    tree += ((all_tokens[saved_index], (ident, fn_args, ret_type, block)),)
                    real_index = index
                
                case "CALL" | "RETURN" | "EOF" | "CLOSEFILE" | _:
                    arg = get_arg(index + 1, all_tokens, operators)
                    tree += ((token, arg),)
                    while token != '\n':
                        real_index += 1
                        try:
                            token = all_tokens[real_index]
                        except:
                            break

        real_index += 1
                    
    return tree