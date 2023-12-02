#!/usr/bin/env python3

from code import InteractiveConsole
from core import parse, compile, execute
import sys


def interpret(filename):
    with open(filename, "rt") as file:
        inp = file.read()
        if inp:
            try:
                execute(compile(parse(inp)))
            except IndexError as err:
                assert str(err) == "pop from empty list"
                print("Error: empty stack")
            except RuntimeError as err:
                print("Error in", err)


class Repl(InteractiveConsole):
    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            execute(compile(parse(source)))
        except IndexError as err:
            assert str(err) == "pop from empty list"
            print("Error: empty stack")
        except RuntimeError as err:
            print("Error in", err)


def main(argv):
    interpret("src/prelude.spill")
    if len(argv) > 1:
        interpret(argv[1])
    else:
        sys.ps1 = "spill> "
        Repl().interact(banner="", exitmsg="")


if __name__ == "__main__":
    main(sys.argv)
