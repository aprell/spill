import concat, newseq, raise from require "utils"
import words from require "builtin"
import Stack from require "stack"

import char, match, sub, gsub from string
import yield, wrap from coroutine

TOKENS = {
	comment: "%(%s+.-%s+%)",
	number:  "[%+%-]?%d+%.*%d*%f[^%w%p]",
	string:  "\".-\"",
	word:    "%S+"
}

next_token = (input) ->
	-- Skip whitespace
	input = gsub input, "^%s*", ""
	-- Skip comment
	if cmt = match input, "^"..TOKENS.comment
		return next_token sub(input, #cmt+1)
	if tok = match input, "^"..TOKENS.number
		return "number", tonumber(tok), sub(input, #tok+1)
	if tok = match input, "^"..TOKENS.string
		return "string", tok, sub(input, #tok+1)
	if tok = match input, "^"..TOKENS.word
		return "word", tok, sub(input, #tok+1)
	assert(#input == 0) and "<end>"

-- Tokenizer coroutine
tokenize = (input) -> wrap ->
	tok, val, rest = next_token input
	while tok != "<end>"
		yield tok, val
		tok, val, rest = next_token rest

export ds, cs
ds, cs = Stack!, Stack!

local eval

-- Parse tokenized input into a list of actions
-- Stop when reading the special word delim
parse = (toks, delim) ->
	actions = {}
	for tok, val in toks
		if delim and val == delim
			-- actions() calls eval(actions)
			return setmetatable actions, {__call: eval}
		if tok == "number" or tok == "string"
			actions[#actions+1] = "__push"
			actions[#actions+1] = val
		-- tok == "word"
		elseif val == ":"
			for _, w in toks
				words[w] = parse toks, ";"
				break
		elseif val == "[" -- quotation
			actions[#actions+1] = "__push"
			actions[#actions+1] = parse toks, "]"
			-- Add tostring metamethod
			mt = getmetatable actions[#actions]
			mt.__tostring = (quot) -> "[ #{concat quot} ]"
		elseif val == "{" -- sequence
			seq = newseq!
			actions[#actions+1] = "__push"
			for t, v in toks
				if v == "}" then break
				if t ~= "number"
					raise "parse: #{v} is not a number"
				seq[#seq+1] = v
			actions[#actions+1] = seq
		elseif val == "if"
			actions[#actions+1] = "__branch?"
			actions[#actions+1] = "<jmp>"
			cs\push #actions
		elseif val == "else"
			actions[#actions+1] = "__branch"
			actions[#actions+1] = "<jmp>"
			actions[cs\pop!] = #actions+1
			cs\push #actions
		elseif val == "then"
			actions[cs\pop!] = #actions+1
		elseif val == "begin"
			cs\push #actions+1
		elseif val == "until"
			actions[#actions+1] = "__branch?"
			actions[#actions+1] = cs\pop!
		else
			actions[#actions+1] = val
	actions

-- Evaluate actions
eval = (actions) ->
	ip = 1 -- "instruction pointer"
	while ip <= #actions
		a = actions[ip]
		if a == "__push"
			words.__push ds, actions[ip+1]
			ip = ip+2
		elseif a == "__branch?"
			if words.__branch ds then ip = actions[ip+1]
			else ip = ip+2
		elseif a == "__branch"
			ip = actions[ip+1]
		else -- built-in or user-defined word
			if words[a] == nil
				raise "eval: #{a} is undefined"
			words[a] ds
			ip = ip+1
	return

{ :tokenize, :parse, :eval }
