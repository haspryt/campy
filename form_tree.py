operators = [
'+', '-', '*', '/', '>', '<', '=', '<>', '<=', '>=', '<-', '&',
"DECLARE", "OUTPUT", "INPUT", "IF", "ELSE", "CASE", "OTHERWISE", "FOR", "NEXT", "REPEAT", "UNTIL", "WHILE", "PROCEDURE", "CALL", "FUNCTION", "RETURN", "TYPE", "OPENFILE", "CLOSEFILE", "READFILE", "EOF", "WRITEFILE", "SEEK", "GETRECORD", "PUTRECORD", "CLASS", "PRIVATE", "PUBLIC",
"RIGHT", "LENGTH", "MID", "LCASE", "UCASE", "INT", "RAND", "DIV", "MOD", "STEP"
]

guide_tokens = ["ENDIF", "ENDCASE", "ENDWHILE", "ENDPROCEDURE", "ENDFUNCTION", "ENDTYPE", "ENDCLASS", "THEN", "TO", "OF"]

def get_user_def_operators(all_tokens: list):
    for token in all_tokens:
        if token == "FUNCTION" or token == "PROCEDURE":
            operators.append(all_tokens[token + 1])