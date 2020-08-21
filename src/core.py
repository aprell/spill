#import concat, newseq, raise from require "utils"
#import words from require "builtin"
#import Stack from require "stack"

#import char, match, sub, gsub from string
#import yield, wrap from coroutine

from builtin import words
import re
import utils

#TOKENS = {
#	comment: "%(%s+.-%s+%)",
#	number:  "[%+%-]?%d+%.*%d*%f[^%w%p]",
#	string:  "\".-\"",
#	word:    "%S+"
#}

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

#next_token = (input) ->
#	-- Skip whitespace
#	input = gsub input, "^%s*", ""
#	-- Skip comment
#	if cmt = match input, "^"..TOKENS.comment
#		return next_token sub(input, #cmt+1)
#	if tok = match input, "^"..TOKENS.number
#		return "number", tonumber(tok), sub(input, #tok+1)
#	if tok = match input, "^"..TOKENS.string
#		return "string", tok, sub(input, #tok+1)
#	if tok = match input, "^"..TOKENS.word
#		return "word", tok, sub(input, #tok+1)
#	assert(#input == 0) and "<end>"

def next_token(input):
    inp = input.lstrip()

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

#-- Tokenizer coroutine
#tokenize = (input) -> wrap ->
#	tok, val, rest = next_token input
#	while tok != "<end>"
#		yield tok, val
#		tok, val, rest = next_token rest

def tokenize(input):
    token, input = next_token(input)
    while token.ty != "EOF":
        yield token
        token, input = next_token(input)

#export ds, cs
#ds, cs = Stack!, Stack!

data_stack = []
ctrl_stack = []

#local eval

#-- Parse tokenized input into a list of actions
#-- Stop when reading the special word delim
#parse = (toks, delim) ->
#	actions = {}
#	for tok, val in toks
#		if delim and val == delim
#			-- actions() calls eval(actions)
#			return setmetatable actions, {__call: eval}
#		if tok == "number" or tok == "string"
#			actions[#actions+1] = "__push"
#			actions[#actions+1] = val
#		-- tok == "word"
#		elseif val == ":"
#			for _, w in toks
#				words[w] = parse toks, ";"
#				break
#		elseif val == "[" -- quotation
#			actions[#actions+1] = "__push"
#			actions[#actions+1] = parse toks, "]"
#			-- Add tostring metamethod
#			mt = getmetatable actions[#actions]
#			mt.__tostring = (quot) -> "[ #{concat quot} ]"
#		elseif val == "{" -- sequence
#			seq = newseq!
#			actions[#actions+1] = "__push"
#			for t, v in toks
#				if v == "}" then break
#				if t ~= "number"
#					raise "parse: #{v} is not a number"
#				seq[#seq+1] = v
#			actions[#actions+1] = seq
#		elseif val == "if"
#			actions[#actions+1] = "__branch?"
#			actions[#actions+1] = "<jmp>"
#			cs\push #actions
#		elseif val == "else"
#			actions[#actions+1] = "__branch"
#			actions[#actions+1] = "<jmp>"
#			actions[cs\pop!] = #actions+1
#			cs\push #actions
#		elseif val == "then"
#			actions[cs\pop!] = #actions+1
#		elseif val == "begin"
#			cs\push #actions+1
#		elseif val == "until"
#			actions[#actions+1] = "__branch?"
#			actions[#actions+1] = cs\pop!
#		else
#			actions[#actions+1] = val
#	actions

def parse(tokens, delim=None):
    cmds = []

    for token in tokens:
        if delim and token.value == delim:
            return lambda _: evaluate(cmds)
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

#-- Evaluate actions
#eval = (actions) ->
#	ip = 1 -- "instruction pointer"
#	while ip <= #actions
#		a = actions[ip]
#		if a == "__push"
#			words.__push ds, actions[ip+1]
#			ip = ip+2
#		elseif a == "__branch?"
#			if words.__branch ds then ip = actions[ip+1]
#			else ip = ip+2
#		elseif a == "__branch"
#			ip = actions[ip+1]
#		else -- built-in or user-defined word
#			if words[a] == nil
#				raise "eval: #{a} is undefined"
#			words[a] ds
#			ip = ip+1
#	return

def evaluate(cmds):
    ip = 0
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
            try:
                words[cmd](data_stack)
            except KeyError:
                raise RuntimeError(f"eval: {cmd} is undefined")
            ip += 1

#{ :tokenize, :parse, :eval }
