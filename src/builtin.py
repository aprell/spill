import math
import utils

words = {}

def builtin(name):
    def register(func):
        words[name] = func
        return func
    return register

@builtin("+")
def builtin_add(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a + b)

@builtin("-")
def builtin_sub(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a - b)

@builtin("*")
def builtin_mul(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a * b)

@builtin("/")
def builtin_div(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a / b)

@builtin("%")
def builtin_mod(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a % b)

@builtin("^")
def builtin_pow(stack):
    b = stack.pop()
    a = stack.pop()
    stack.append(a ** b)

@builtin("=")
def builtin_eq(stack):
    b = stack.pop()
    a = stack.pop()
    if a == b:
        stack.append(1)
    else:
        stack.append(0)

@builtin("!=")
def builtin_ne(stack):
    b = stack.pop()
    a = stack.pop()
    if a != b:
        stack.append(1)
    else:
        stack.append(0)

@builtin("<")
def builtin_lt(stack):
    b = stack.pop()
    a = stack.pop()
    if a < b:
        stack.append(1)
    else:
        stack.append(0)

@builtin("<=")
def builtin_lte(stack):
    b = stack.pop()
    a = stack.pop()
    if a <= b:
        stack.append(1)
    else:
        stack.append(0)

@builtin(">")
def builtin_gt(stack):
    b = stack.pop()
    a = stack.pop()
    if a > b:
        stack.append(1)
    else:
        stack.append(0)

@builtin(">=")
def builtin_gte(stack):
    b = stack.pop()
    a = stack.pop()
    if a >= b:
        stack.append(1)
    else:
        stack.append(0)

@builtin("abs")
def builtin_abs(stack):
    stack.append(abs(stack.pop()))

@builtin("ceil")
def builtin_ceil(stack):
    stack.append(math.ceil(stack.pop()))

@builtin("floor")
def builtin_floor(stack):
    stack.append(math.floor(stack.pop()))

@builtin("pi")
def builtin_pi(stack):
    stack.append(math.pi)

@builtin("e")
def builtin_e(stack):
    stack.append(math.e)

@builtin("ln")
def builtin_ln(stack):
    "Base-e logarithm"
    stack.append(math.log(stack.pop()))

@builtin("log")
def builtin_log(stack):
    "Base-10 logarithm"
    stack.append(math.log10(stack.pop()))

@builtin("log2")
def builtin_log2(stack):
    "Base-2 logarithm"
    stack.append(math.log2(stack.pop()))

@builtin("min")
def builtin_min(stack):
    stack.append(min(stack.pop(), stack.pop()))

@builtin("max")
def builtin_max(stack):
    stack.append(max(stack.pop(), stack.pop()))

@builtin("dup")
def builtin_dup(stack):
    "Duplicate top of stack"
    stack.append(stack[-1])

@builtin("drop")
def builtin_drop(stack):
    "Discard top of stack"
    stack.pop()

@builtin("nip")
def builtin_nip(stack):
    "Discard element below top of stack"
    t = stack.pop()
    stack.pop()
    stack.append(t)

@builtin("clear")
def builtin_clear(stack):
    "Discard entire stack"
    stack.clear()

@builtin("print")
def builtin_print_top(stack):
    "Print top of stack"
    print(stack[-1])

@builtin(".")
def builtin_print_pop(stack):
    "Print and discard top of stack"
    print(stack.pop())

@builtin("show")
def builtin_show(stack):
    "Print entire stack"
    print("[" + utils.concat(stack, sep=", ") + "]")

@builtin("swap")
def builtin_swap(stack):
    "Swap topmost elements"
    b = stack.pop()
    a = stack.pop()
    stack += [b, a]

@builtin("over")
def builtin_over(stack):
    """
    Duplicate element below top of stack:
    `a b over` is equivalent to `a b a`
    """
    b = stack.pop()
    a = stack.pop()
    stack += [a, b, a]

@builtin("rot")
def builtin_rot(stack):
    """
    Rotate topmost elements:
    `a b c rot` is equivalent to `b c a`
    """
    c = stack.pop()
    builtin_swap(stack)
    stack.append(c)
    builtin_swap(stack)

@builtin("cr")
def builtin_cr(_):
    "Print newline"
    print()

@builtin("elems")
def builtin_elems(stack):
    stack.append(len(stack))

@builtin("__push")
def builtin___push(stack, data):
    stack.append(data)

@builtin("__branch")
def builtin___branch(stack):
    "Conditional branch (branch if false)"
    if stack.pop() == 0:
        return True
    else:
        return False

#
# COMBINATORS
#

@builtin("times")
def builtin_times(stack):
    "Apply quotation `f` `n` times"
    f = stack.pop()
    n = stack.pop()
    for _ in range(1, n + 1):
        f(stack)

@builtin("keep")
def builtin_keep(stack):
    "Apply quotation `f` to `x` and put `x` back on top of the stack"
    f = stack.pop()
    x = stack[-1]
    f(stack)
    stack.append(x)

@builtin("dip")
def builtin_dip(stack):
    "Apply quotation `f` to the element below the top of the stack"
    f = stack.pop()
    x = stack.pop()
    f(stack)
    stack.append(x)

@builtin("bi")
def builtin_bi(stack):
    "Cleave combinator: apply quotations `f` and `g` to `x`"
    g = stack.pop()
    builtin_keep(stack)
    g(stack)

@builtin("bi*")
def builtin_bi_star(stack):
    "Spread combinator: apply quotations `f` to `x` and `g` to `y`"
    g = stack.pop()
    builtin_dip(stack)
    g(stack)

@builtin("bi@")
def builtin_bi_at(stack):
    "Apply combinator: apply quotation `f` to `x` and then to `y`"
    f = stack[-1]
    builtin_dip(stack)
    f(stack)

#
# SEQUENCE OPERATORS
#

@builtin("length")
def builtin_length(stack):
    "Get length of sequence"
    stack.append(len(stack.pop()))

@builtin("range")
def builtin_range(stack):
    "Create sequence from range"
    step = stack.pop()
    stop = stack.pop()
    start = stack.pop()
    stack.append(
        utils.Sequence(list(range(start, stop + 1, step)))
    )

@builtin("mkseq")
def builtin_mkseq(stack):
    "Create sequence from `n` numbers on the stack"
    seq = utils.Sequence()
    n = stack.pop()
    for _ in range(1, n + 1):
        seq.append(stack.pop())
    seq.reverse()
    stack.append(seq)

@builtin("!!")
def builtin_index(stack):
    "Index into sequence"
    n = stack.pop()
    seq = stack.pop()
    if not 0 <= n < len(seq):
        raise RuntimeError(f"!!: index {n} is out of bounds")
    stack.append(seq[n])

@builtin("each")
def builtin_each(stack):
    "Apply quotation `f` to each value in a sequence"
    f = stack.pop()
    seq = stack.pop()
    for number in seq:
        stack.append(number)
        f(stack)

@builtin("filter")
def builtin_filter(stack):
    "Filter sequence"
    fseq = utils.Sequence()
    p = stack.pop()
    seq = stack.pop()
    for number in seq:
        stack.append(number)
        p(stack)
        if stack.pop() == 1:
            fseq.append(number)
    stack.append(fseq)
