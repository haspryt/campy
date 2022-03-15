from tokenizer import tokenize
from form_tree import form_tree, get_user_def_operators
from destructure_tree import destructure_tree
from checks import syntax_check, loop_check
import sys

def main():
    operators = [
        '+', '-', '*', '/', '>', '<', '=', '<>', '<=', '>=', '<-', '&', ',', "AND", "NOT", "OR",
        "DECLARE", "OUTPUT", "IF", "ELSE", "CASE", "OTHERWISE", "FOR", "REPEAT", "UNTIL", "WHILE", "PROCEDURE", "CALL", "FUNCTION", "RETURN", "TYPE", "OPENFILE", "CLOSEFILE", "READFILE", "EOF", "WRITEFILE", "SEEK", "GETRECORD", "PUTRECORD", "CLASS", "PRIVATE", "PUBLIC",
        "RIGHT", "LENGTH", "MID", "LCASE", "UCASE", "INT", "RAND", "DIV", "MOD", "STEP"
    ]

    try:
        to_open = sys.argv[1]
    except:
        to_open = "example_text.cpc"
    
    try:
        out_file = sys.argv[2]
    except:
        out_file = "a.py"

    test = open(to_open, "r").read()
    syntax_check(to_open)
    loop_check(to_open)

    tokens = tokenize(test)
    get_user_def_operators(tokens, operators)
    tree = form_tree(tokens, operators)

    #for t in tree:
    #    print(t)

    if type(tree[0]) == str: 
        source = destructure_tree(tree, 0, operators)
    else:
        source = destructure_tree(tree, -1, operators)

    #print(source)
    f = open(out_file, 'w')
    f.write(source)
    f.close()

if __name__ == '__main__':
    main()