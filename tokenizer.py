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
        re.compile(r"^[?!.@^~`'_|\/#$&{}+*:,><=()-]"),
        re.compile(r"^[\"]"),
        re.compile(r"^\n"),
        re.compile(r"^ "),
    ]

    while len(string):
        match = False

        for token_re in token_rex:
            mo = token_re.match(string)
            if mo:
                match = True
                token = mo.group(0)
                all_tokens.append(token)
                string = token_re.sub('', string)
                break
    
    index = 0
    saved_index = 0
    ap_counter = 0
    while True:
        try:
            token = all_tokens[index]
        except:
            all_tokens = list(filter((" ").__ne__, all_tokens))
            return all_tokens
        if token == "\"":
            ap_counter += 1
            if ap_counter % 2 == 1:
                saved_index = index
            else:
                new_t = ""
                for i in range(saved_index, index+1):
                    new_t = new_t + ''.join(all_tokens[i])
                for _ in range(saved_index, index):
                    del all_tokens[saved_index]
                all_tokens[saved_index] = new_t
                index = saved_index + 1
        index += 1