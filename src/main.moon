package.moonpath = "src/?.moon;" .. package.moonpath

import tokenize, parse, eval from require "core"
import words from require "builtin"

interpret = (filename) ->
	file = assert(io.open filename)
	inp = file\read "*all"
	if #inp > 0
		ok, err = pcall -> eval parse tokenize inp
		if not ok then print err
	file\close!

-- Read-eval-print loop
repl = (prompt = "spill> ") ->
	while true
		io.write prompt
		inp = io.read!
		unless inp
			io.write "\n"
			break
		if #inp > 0
			ok, err = pcall -> eval parse tokenize inp
			if not ok then print err

main = (...) ->
	interpret "src/prelude.spl"
	if #arg > 0 then interpret arg[1] else repl!

main ...
