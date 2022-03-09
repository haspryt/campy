from tokenizer import tokenize
from form_tree import form_tree, get_user_def_operators
from destructure_tree import destructure_tree
from checks import syntax_check, loop_check

operators = [
    '+', '-', '*', '/', '>', '<', '=', '<>', '<=', '>=', '<-', '&', "AND", "NOT", "OR",
    "DECLARE", "OUTPUT", "IF", "ELSE", "CASE", "OTHERWISE", "FOR", "REPEAT", "UNTIL", "WHILE", "PROCEDURE", "CALL", "FUNCTION", "RETURN", "TYPE", "OPENFILE", "CLOSEFILE", "READFILE", "EOF", "WRITEFILE", "SEEK", "GETRECORD", "PUTRECORD", "CLASS", "PRIVATE", "PUBLIC",
    "RIGHT", "LENGTH", "MID", "LCASE", "UCASE", "INT", "RAND", "DIV", "MOD", "STEP"
]

test = open("example_text.cpc", "r").read()


syntax_check("example_text.cpc")
loop_check("example_text.cpc")

tokens = tokenize(test)
get_user_def_operators(tokens, operators)
tree = form_tree(tokens, operators)

for t in tree:
    print(t)

if type(tree[0]) == str: 
    source = destructure_tree(tree, 0, operators)
else:
    source = destructure_tree(tree, -1, operators)

print(source)