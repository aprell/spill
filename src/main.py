#!/usr/bin/env python3

from core import tokenize, parse, evaluate
import sys

def interpret(filename):
    with open(filename, "rt") as file:
        inp = file.read()
        if inp:
            evaluate(parse(tokenize(inp)))

def repl(prompt="spill> "):
    "The spill read-eval-print loop"
    try:
        while True:
            inp = input(prompt)
            if inp:
                evaluate(parse(tokenize(inp)))
    except EOFError:
        print()

def main(argv):
    interpret("src/prelude.spill")
    if len(argv) > 1:
        interpret(argv[1])
    else:
        repl()

if __name__ == "__main__":
    main(sys.argv)
