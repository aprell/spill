from builtin import words
import re
import utils

TOKENS = {
    "comment": re.compile(r"\(\s+.*\s+\)"),
    "number": re.compile(r"[+-]?\d+(\.\d*)?\b"),
    "string": re.compile(r"\"(.*?)\""),
    "word": re.compile(r"\S+")
}

class Token:
    def __init__(self, ty, value):
        self.ty = ty
        self.value = value

    def __repr__(self):
        return f"Token({self.ty}, {self.value})"

def next_token(input):
    # Skip whitespace
    inp = input.lstrip()

    # Skip comment
    match = TOKENS["comment"].match(inp)
    if match:
        return next_token(inp[match.end():])

    match = TOKENS["number"].match(inp)
    if match:
        num = match.group()
        try:
            num = int(num)
        except ValueError:
            num = float(num)
        return Token("number", num), inp[match.end():]

    match = TOKENS["string"].match(inp)
    if match:
        return Token("string", match.group(1)), inp[match.end():]

    match = TOKENS["word"].match(inp)
    if match:
        return Token("word", match.group()), inp[match.end():]

    assert not inp
    return Token("EOF", None), inp

def tokenize(input):
    "Yield tokens from input string"
    token, input = next_token(input)
    while token.ty != "EOF":
        yield token
        token, input = next_token(input)

data_stack = []
ctrl_stack = []

class Commands:
    def __init__(self, lst=[]):
        self.cmds = lst

    def __call__(self, _):
        evaluate(self.cmds)

    def __iter__(self):
        return iter(self.cmds)

    def __len__(self):
        return len(self.cmds)

    def __str__(self):
        return f"[ {utils.concat(self.cmds)} ]"

def parse(tokens, delim=None):
    "Turn tokens into a list of commands to evaluate"
    cmds = []

    for token in tokens:
        if delim and token.value == delim:
            return Commands(cmds)
        if token.ty == "number" or token.ty == "string":
            cmds += ["__push", token.value]
        elif token.value == ":":
            name = next(tokens).value
            words[name] = parse(tokens, delim=";")
        elif token.value == "[":
            cmds += ["__push", parse(tokens, delim="]")]
        elif token.value == "{":
            cmds.append("__push")
            seq = utils.Sequence()
            for token in tokens:
                if token.value == "}":
                    break
                if token.ty != "number":
                    raise RuntimeError(f"parse: {token.value} is not a number")
                seq.append(token.value)
            cmds.append(seq)
        elif token.value == "if":
            cmds += ["__branch?", "<jmp>"]
            ctrl_stack.append(len(cmds) - 1)
        elif token.value == "else":
            cmds += ["__branch", "<jmp>"]
            cmds[ctrl_stack.pop()] = len(cmds)
            ctrl_stack.append(len(cmds) - 1)
        elif token.value == "then":
            cmds[ctrl_stack.pop()] = len(cmds)
        elif token.value == "begin":
            ctrl_stack.append(len(cmds))
        elif token.value == "until":
            cmds += ["__branch?", ctrl_stack.pop()]
        else:
            cmds.append(token.value)

    return cmds

def evaluate(cmds):
    "Evaluate list of commands"
    ip = 0 # "Instruction pointer"
    while ip < len(cmds):
        cmd = cmds[ip]
        if cmd == "__push":
            words["__push"](data_stack, cmds[ip+1])
            ip += 2
        elif cmd == "__branch":
            ip = cmds[ip+1]
        elif cmd == "__branch?":
            if words["__branch"](data_stack):
                ip = cmds[ip+1]
            else:
                ip += 2
        else:
            # Built-in or user-defined word
            try:
                words[cmd](data_stack)
            except KeyError:
                raise RuntimeError(f"eval: {cmd} is undefined")
            ip += 1
