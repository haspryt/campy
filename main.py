from tokenizer import tokenize
test = open("example_text.cpc", "r").read()

tokens = tokenize(test)
print(tokens)