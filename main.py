from tokenizer import tokenize
from form_tree import form_tree, get_user_def_operators
from destructure_tree import destructure_tree

operators = [
    '+', '-', '*', '/', '>', '<', '=', '<>', '<=', '>=', '<-', '&', "AND", "NOT", "OR",
    "DECLARE", "OUTPUT", "IF", "ELSE", "CASE", "OTHERWISE", "FOR", "REPEAT", "UNTIL", "WHILE", "PROCEDURE", "CALL", "FUNCTION", "RETURN", "TYPE", "OPENFILE", "CLOSEFILE", "READFILE", "EOF", "WRITEFILE", "SEEK", "GETRECORD", "PUTRECORD", "CLASS", "PRIVATE", "PUBLIC",
    "RIGHT", "LENGTH", "MID", "LCASE", "UCASE", "INT", "RAND", "DIV", "MOD", "STEP"
]

test = open("example_text.cpc", "r").read()

tokens = tokenize(test)
get_user_def_operators(tokens, operators)
tree = form_tree(tokens, operators)
#print(tree)
#print("-------------------")
if type(tree[0]) == str: 
    source = destructure_tree(tree, 0, operators)
else:
    source = destructure_tree(tree, -1, operators)
#print("-------------------")
print(source)
#for i in tree:
#    print(i)