operators = [
'+', '-', '*', '/', '>', '<', '=', '<>', '<=', '>=', '<-', '&', "AND", "NOT", "OR"
"DECLARE", "OUTPUT", "INPUT", "IF", "ELSE", "CASE", "OTHERWISE", "FOR", "NEXT", "REPEAT", "UNTIL", "WHILE", "PROCEDURE", "CALL", "FUNCTION", "RETURN", "TYPE", "OPENFILE", "CLOSEFILE", "READFILE", "EOF", "WRITEFILE", "SEEK", "GETRECORD", "PUTRECORD", "CLASS", "PRIVATE", "PUBLIC",
"RIGHT", "LENGTH", "MID", "LCASE", "UCASE", "INT", "RAND", "DIV", "MOD", "STEP"
]

guide_tokens = ["ENDIF", "ENDCASE", "ENDWHILE", "ENDPROCEDURE", "ENDFUNCTION", "ENDTYPE", "ENDCLASS", "THEN", "TO", "OF"]

def get_user_def_operators(all_tokens: list):
    for token in all_tokens:
        if token == "FUNCTION" or token == "PROCEDURE":
            operators.append(all_tokens[token + 1])


def get_arg(index: int, all_tokens: list):
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
            return form_tree(all_tokens[slice(saved_index + 1, index)])
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
            return form_tree(all_tokens[slice(index + 1, saved_index)])
        case _:
            return all_tokens[index]


def form_tree(all_tokens: list):
    operators = get_user_def_operators(all_tokens)
    for (index, token) in enumerate(all_tokens):
        if token in operators:
            current_operator = token
            match token:
                case '+'| '-' | '*' | '/' | '>' | '<' | '=' | '<>' | '<=' | '>=' | '<-' | '&' | "AND" | "NOT" | "OR":
                    args = (get_arg(index - 1, all_tokens), get_arg(index + 1, all_tokens))
                    return (token, args)
                case "IF":
                    saved_index = index
                    current = token
                    while current != "THEN":
                        index += 1
                        current = all_tokens[index]
                    condition = form_tree(all_tokens[slice(saved_index + 1, index)])