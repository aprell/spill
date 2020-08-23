spill
=====

spill is a tiny stack-based programming language that borrows ideas from Forth
and Factor. The interpreter is written in Python.
A [previous version](https://github.com/aprell/spill/tree/5a2546a) of spill
was implemented in the [MoonScript](http://moonscript.org) dialect of Lua.

Examples
--------

Start the REPL with `./spill`.

Say hello:

```
spill> "Hello, spill!" print
Hello, spill!
```

Evaluate simple expressions:

```
spill> 1 2 3 + / .
0.2
```

Define and use functions:

```
spill> : ++ 1 + ;
spill> 42 ++ .
43
```

Apply quotations with combinators:

```
spill> 1 2 3 [ ++ ] dip
spill> show
[1, 3, 3]
```

Inspect generated bytecode:

```
spill> [ 3 0 > if "yes" else "no" then . ] spill show
[__push, 3, __push, 0, >, __branch?, 11, __push, yes, __branch, 13, __push, no, .]
```

Check `src/prelude.spl` for more examples.

TODO
----

Stuff that could be added to make the language more useful:
- Stack effect comments
- Better control constructs
- Proper support for strings and sequences
- Map/dictionary data type
- Vocabularies of words

References
----------

- [My history with Forth & stack machines](http://yosefk.com/blog/my-history-with-forth-stack-machines.html)
- [A simple stack-oriented language](http://www.openbookproject.net/py4fun/forth/forth.html)
- [Beginning Factor - Introduction](http://elasticdog.com/2008/11/beginning-factor-introduction)
- [Beginning Factor - Shufflers & Combinators](http://elasticdog.com/2008/12/beginning-factor-shufflers-and-combinators)
- [A panoramic tour of Factor](http://andreaferretti.github.io/factor-tutorial)
- [A simple Python token scanner](https://gist.github.com/blinks/47989)
