import tokenize, parse, eval from require "spill"
import words from require "builtin"

interpret = (filename) ->
	file = assert(io.open filename)
	inp = file\read "*all"
	if #inp > 0 then io.write eval parse tokenize inp
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
			io.write eval parse tokenize inp
			io.write "Data stack: ", words.dump ds

main = (...) ->
	interpret "prelude.spl"
	args = {...}
	if #args > 0 then interpret args[1] else repl!

main ...
