import re

def tokenize(string: str):
    all_tokens = []
    token_rex = [
        re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*"),
        re.compile(r"^[0-9]+"),
        re.compile(r"^<<"),
        re.compile(r"^>="),
        re.compile(r"^<="),
        re.compile(r"^//"),
        re.compile(r"^[?!.@^~`'_|\/#$&{}+*:,><-]"),
        re.compile(r"^[()]"),
        re.compile(r"^[\"]"),
        re.compile(r"^\n"),
        re.compile(r"^="),
    ]

    while len(string):
        string = string.lstrip(" ")
        match = False

        for token_re in token_rex:
            mo = token_re.match(string)
            if mo:
                match = True
                token = mo.group(0)
                all_tokens.append(token)
                string = token_re.sub('', string)
                break
    return all_tokens