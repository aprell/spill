import tokenize, parse, eval from require "spill"
import words from require "builtin"
require "prelude"

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

main = -> repl!

main!
