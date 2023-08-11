from builtin import words, memory
import re
import utils


class Token:
    def __init__(self, match):
        self.type = match.lastgroup
        self.value = match.group()
        if self.type == "NUMBER":
            try:
                self.value = int(self.value)
            except ValueError:
                self.value = float(self.value)
        elif self.type == "STRING":
            self.value = self.value[1:-1]

    def __repr__(self):
        return f"Token({self.type}: {self.value})"


class Tokenizer:
    def __init__(self, **tokens):
        self.tokens = tokens
        self.__compile()
        self.ignores = set()

    def __compile(self):
        self.regex = re.compile("|".join(
            f"(?P<{name}>{pattern})" for name, pattern in self.tokens.items()
        ))

    def __call__(self, string):
        while string:
            # Skip whitespace
            string = string.lstrip()
            match = self.regex.match(string)
            if match:
                string = string[match.end():]
                # Skip comments
                if match.lastgroup not in self.ignores:
                    yield Token(match)
            else:
                assert not string

    def ignore(self, name):
        self.ignores.add(name)


def tokenize(string):
    "Yield tokens from input string"
    tokenizer = Tokenizer(
        COMMENT=r"\(\s+[^\)]*\s+\)",
        NUMBER=r"[+-]?\d+(?:\.\d*)?\b",
        STRING=r"\".*?\"",
        WORD=r"\S+"
    )
    tokenizer.ignore("COMMENT")
    return (token for token in tokenizer(string))


data_stack = []
ctrl_stack = []


class Commands:
    def __init__(self, lst=None):
        self.cmds = lst if lst else []

    def __call__(self, _):
        evaluate(self.cmds)

    def __iter__(self):
        return iter(self.cmds)

    def __len__(self):
        return len(self.cmds)

    def __repr__(self):
        return f"[ {utils.concat(self.cmds)} ]"


def parse(tokens, delim=None):
    "Turn tokens into a list of commands to evaluate"
    cmds = []

    for token in tokens:
        if delim and token.value == delim:
            return Commands(cmds)
        if token.type == "NUMBER" or token.type == "STRING":
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
                if token.type != "NUMBER":
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
    ip = 0  # "Instruction pointer"
    while ip < len(cmds):
        cmd = cmds[ip]
        if cmd == "__push":
            words["__push"](data_stack, cmds[ip+1])
            ip += 2
        elif cmd == "__branch":
            ip = cmds[ip + 1]
        elif cmd == "__branch?":
            if words["__branch"](data_stack):
                ip = cmds[ip + 1]
            else:
                ip += 2
        elif cmd == "variable":
            var = cmds[ip + 1]
            words[var] = Commands(["__push", var])
            memory[var] = None  # Uninitialized
            ip += 2
        else:
            # Built-in or user-defined word
            try:
                words[cmd](data_stack)
            except KeyError:
                raise RuntimeError(f"eval: {cmd} is undefined")
            ip += 1
