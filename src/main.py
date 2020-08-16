#!/usr/bin/env python3

#package.moonpath = "src/?.moon;" .. package.moonpath

#import tokenize, parse, eval from require "core"
#import words from require "builtin"

from core import tokenize, parse, evaluate

import sys

#interpret = (filename) ->
#	file = assert(io.open filename)
#	inp = file\read "*all"
#	if #inp > 0
#		ok, err = pcall -> eval parse tokenize inp
#		if not ok then print err
#	file\close!

def interpret(filename):
    with open(filename, "rt") as file:
        inp = file.read()
        if inp:
            evaluate(parse(tokenize(inp)))

#-- Read-eval-print loop
#repl = (prompt = "spill> ") ->
#	while true
#		io.write prompt
#		inp = io.read!
#		unless inp
#			io.write "\n"
#			break
#		if #inp > 0
#			ok, err = pcall -> eval parse tokenize inp
#			if not ok then print err

# Read-eval-print loop
def repl(prompt="spill> "):
    try:
        while True:
            inp = input(prompt)
            if inp:
                evaluate(parse(tokenize(inp)))
    except EOFError:
        print()

#main = (...) ->
#	interpret "src/prelude.spl"
#	if #arg > 0 then interpret arg[1] else repl!
#
#main ...

def main(argv):
    #interpret("src/prelude.spl")
    if len(argv) > 1:
        interpret(argv[1])
    else:
        repl()

if __name__ == "__main__":
    main(sys.argv)
