#import reverse, newseq, raise from require "utils"

import math
import utils

words = {}

def builtin(name):
    def register(func):
        words[name] = func
        return func
    return register

#builtin_words = {

    #-- Operator "+"
    #["+"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push a + b

@builtin("+")
def builtin_add(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a + b)

    #-- Operator "-"
    #["-"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push a - b

@builtin("-")
def builtin_sub(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a - b)

    #-- Operator "*"
    #["*"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push a * b

@builtin("*")
def builtin_mul(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a * b)

    #-- Operator "/"
    #["/"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push a / b

@builtin("/")
def builtin_div(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a / b)

    #-- Operator "%" (modulo)
    #["%"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push a % b

@builtin("%")
def builtin_mod(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a % b)

    #-- Operator "^" (exponentiation)
    #["^"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push a ^ b

@builtin("^")
def builtin_pow(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a ** b)

    #-- Operator "="
    #["="]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	if a == b then s\push 1 else s\push 0

@builtin("=")
def builtin_eq(stack):
    b = stack.pop()
    a = stack.pop()
    if a == b:
        stack.append(1)
    else:
        stack.append(0)

    #-- Operator "!="
    #["!="]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	if a != b then s\push 1 else s\push 0

@builtin("!=")
def builtin_ne(stack):
    b = stack.pop()
    a = stack.pop()
    if a != b:
        stack.append(1)
    else:
        stack.append(0)

    #-- Operator "<"
    #["<"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	if a < b then s\push 1 else s\push 0

@builtin("<")
def builtin_lt(stack):
    b = stack.pop()
    a = stack.pop()
    if a < b:
        stack.append(1)
    else:
        stack.append(0)

    #-- Operator "<="
    #["<="]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	if a <= b then s\push 1 else s\push 0

@builtin("<=")
def builtin_lte(stack):
    b = stack.pop()
    a = stack.pop()
    if a <= b:
        stack.append(1)
    else:
        stack.append(0)

    #-- Operator ">"
    #[">"]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	if a > b then s\push 1 else s\push 0

@builtin(">")
def builtin_gt(stack):
    b = stack.pop()
    a = stack.pop()
    if a > b:
        stack.append(1)
    else:
        stack.append(0)

    #-- Operator ">="
    #[">="]: (s) ->
    #	b, a = s\pop!, s\pop!
    #	if a >= b then s\push 1 else s\push 0

@builtin(">=")
def builtin_gte(stack):
    b = stack.pop()
    a = stack.pop()
    if a >= b:
        stack.append(1)
    else:
        stack.append(0)

    #abs: (s) -> s\push math.abs s\pop!

@builtin("abs")
def builtin_abs(stack):
    stack.append(abs(stack.pop()))

    #ceil: (s) -> s\push math.ceil s\pop!

@builtin("ceil")
def builtin_ceil(stack):
    stack.append(math.ceil(stack.pop()))

    #floor: (s) -> s\push math.floor s\pop!

@builtin("floor")
def builtin_floor(stack):
    stack.append(math.floor(stack.pop()))

    #pi: (s) -> s\push math.pi

@builtin("pi")
def builtin_pi(stack):
    stack.append(math.pi)

    #e: (s) -> s\push math.exp 1

@builtin("e")
def builtin_e(stack):
    stack.append(math.e)

    #-- Base e logarithm
    #ln: (s) -> s\push math.log s\pop!

@builtin("ln")
def builtin_ln(stack):
    stack.append(math.log(stack.pop()))

    #-- Base 10 logarithm
    #log: (s) -> s\push math.log10 s\pop!

@builtin("log")
def builtin_log(stack):
    stack.append(math.log10(stack.pop()))

    #-- Base 2 logarithm
    #log2: (s) -> s\push (math.log10 s\pop!) / (math.log10 2)

@builtin("log2")
def builtin_log2(stack):
    stack.append(math.log2(stack.pop()))

    #min: (s) -> s\push math.min s\pop!, s\pop!

@builtin("min")
def builtin_min(stack):
    stack.append(min(stack.pop(), stack.pop()))

    #max: (s) -> s\push math.max s\pop!, s\pop!

@builtin("max")
def builtin_max(stack):
    stack.append(max(stack.pop(), stack.pop()))

    #-- Duplicate top of stack
    #dup: (s) -> s\push s\top!

@builtin("dup")
def builtin_dup(stack):
    stack.append(stack[-1])

    #-- Discard top of stack
    #drop: (s) -> s\pop!

@builtin("drop")
def builtin_drop(stack):
    stack.pop()

    #-- Discard element below top of stack
    #nip: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push b

@builtin("nip")
def builtin_nip(stack):
    t = stack.pop()
    stack.pop()
    stack.append(t)

    #-- Discard entire stack
    #clear: (s) -> while not s\isempty! do s\pop!

@builtin("clear")
def builtin_clear(stack):
    stack.clear()

    #-- Print top of stack
    #print: (s) -> io.write (tostring s\top!), "\n"

@builtin("print")
def builtin_print_top(stack):
    print(stack[-1])

    #-- Print and remove top of stack
    #["."]: (s) -> io.write (tostring s\pop!), "\n"

@builtin(".")
def builtin_print_pop(stack):
    print(stack.pop())

    #-- Print stack
    #show: (s) -> print s

@builtin("show")
def builtin_show(stack):
    print("[" + utils.concat(stack, sep=", ") + "]")

    #-- Swap topmost elements
    #swap: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push b
    #	s\push a

@builtin("swap")
def builtin_swap(stack):
    b = stack.pop()
    a = stack.pop()
    stack += [b, a]

    #-- Duplicate element below top of stack
    #-- 'a b over' is equivalent to 'a b a'
    #over: (s) ->
    #	b, a = s\pop!, s\pop!
    #	s\push a
    #	s\push b
    #	s\push a

@builtin("over")
def builtin_over(stack):
    b = stack.pop()
    a = stack.pop()
    stack += [a, b, a]

    #-- Rotate top three elements
    #-- 'a b c rot' is equivalent to 'b c a'
    #rot: (s) ->
    #	c = s\pop!
    #	words.swap s
    #	s\push c
    #	words.swap s

@builtin("rot")
def builtin_rot(stack):
    c = stack.pop()
    builtin_swap(stack)
    stack.append(c)
    builtin_swap(stack)

    #-- Print newline
    #cr: -> io.write "\n"

@builtin("cr")
def builtin_cr(_):
    print()

    #-- Number of elements of data stack
    #elems: (s) -> s\push #s.elems

@builtin("elems")
def builtin_elems(stack):
    stack.append(len(stack))

    #-- Push data onto stack
    #__push: (s, d) -> s\push d

@builtin("__push")
def builtin___push(stack, data):
    stack.append(data)

    #-- Conditional branch: branch on false
    #__branch: (s) -> if s\pop! == 0 then true else false

@builtin("__branch")
def builtin___branch(stack):
    if stack.pop() == 0:
        return True
    else:
        return False

    #-- Conditional branch: branch on true
    #-- TODO

    #--------------------------------------------------------------------------
    #-- Combinators
    #--------------------------------------------------------------------------

    #-- Apply quotation f n times
    #times: (s) ->
    #	f, n = s\pop!, s\pop!
    #	for i = 1, n do f s

@builtin("times")
def builtin_times(stack):
    f = stack.pop()
    n = stack.pop()
    for _ in range(1, n + 1):
        f(stack)

    #-- Apply quotation f to x and put x back on top of the stack
    #keep: (s) ->
    #	f, x = s\pop!, s\top!
    #	f s
    #	s\push x

@builtin("keep")
def builtin_keep(stack):
    f = stack.pop()
    x = stack[-1]
    f(stack)
    stack.append(x)

    #-- Apply quotation f to the element below the top of the stack
    #dip: (s) ->
    #	f, x = s\pop!, s\pop!
    #	f s
    #	s\push x

@builtin("dip")
def builtin_dip(stack):
    f = stack.pop()
    x = stack.pop()
    f(stack)
    stack.append(x)

    #-- Cleave combinator: Apply quotations f and g to x
    #bi: (s) ->
    #	g = s\pop!
    #	words.keep s
    #	g s

@builtin("bi")
def builtin_bi(stack):
    g = stack.pop()
    builtin_keep(stack)
    g(stack)

    #-- Spread combinator: Apply quotations f to x and g to y
    #["bi*"]: (s) ->
    #	g = s\pop!
    #	words.dip s
    #	g s

@builtin("bi*")
def builtin_bi_star(stack):
    g = stack.pop()
    builtin_dip(stack)
    g(stack)

    #-- Apply combinator: Apply quotation f to x and then to y
    #["bi@"]: (s) ->
    #	f = s\top!
    #	words.dip s
    #	f s

@builtin("bi@")
def builtin_bi_at(stack):
    f = stack[-1]
    builtin_dip(stack)
    f(stack)

    #--------------------------------------------------------------------------
    #-- Sequence operators
    #--------------------------------------------------------------------------

    #-- Get length of sequence
    #length: (s) -> s\push #s\pop!

@builtin("length")
def builtin_length(stack):
    stack.append(len(stack.pop()))

    #-- Create sequence
    #range: (s) ->
    #	seq = newseq!
    #	_step, _end, _start = s\pop!, s\pop!, s\pop!
    #	for i = _start, _end, _step
    #		seq[#seq+1] = i
    #	s\push seq

@builtin("range")
def builtin_range(stack):
    step = stack.pop()
    stop = stack.pop()
    start = stack.pop()
    stack.append(
        utils.Sequence(list(range(start, stop + 1, step)))
    )

    #-- Create sequence from n numbers on the stack
    #mkseq: (s) ->
    #	seq = newseq!
    #	n = s\pop!
    #	for i = 1, n
    #		seq[#seq+1] = s\pop!
    #	s\push reverse seq

@builtin("mkseq")
def builtin_mkseq(stack):
    seq = utils.Sequence()
    n = stack.pop()
    for _ in range(1, n + 1):
        seq.append(stack.pop())
    seq.reverse()
    stack.append(seq)

    #-- Index into sequence
    #["!!"]: (s) ->
    #	n, seq = s\pop!, s\pop!
    #	if n <= 0 or n > #seq
    #		raise "!!: index #{n} out of bounds"
    #	s\push seq[n]

@builtin("!!")
def builtin_index(stack):
    n = stack.pop()
    seq = stack.pop()
    if not 0 <= n < len(seq):
        raise RuntimeError(f"!!: index {n} is out of bounds")
    stack.append(seq[n])

    #-- Apply quotation f to each value v in sequence seq
    #each: (s) ->
    #	f, seq = s\pop!, s\pop!
    #	for _, v in ipairs seq
    #		s\push v
    #		f s

@builtin("each")
def builtin_each(stack):
    f = stack.pop()
    seq = stack.pop()
    for number in seq:
        stack.append(number)
        f(stack)

    #-- Filter sequence
    #filter: (s) ->
    #	fseq = newseq!
    #	p, seq = s\pop!, s\pop!
    #	for _, v in ipairs seq
    #		s\push v
    #		p s
    #		fseq[#fseq+1] = v if s\pop! == 1
    #	s\push fseq

@builtin("filter")
def builtin_filter(stack):
    fseq = utils.Sequence()
    p = stack.pop()
    seq = stack.pop()
    for number in seq:
        stack.append(number)
        p(stack)
        if stack.pop() == 1:
            fseq.append(number)
    stack.append(fseq)

#}

#builtin_words.__index = builtin_words

#setmetatable words, builtin_words

#{ :words }
