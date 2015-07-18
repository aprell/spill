import reverse, newseq, raise from require "util"

words = {}

builtin_words = {

	-- Operator "+"
	["+"]: (s) ->
		b, a = s\pop!, s\pop!
		s\push a + b

	-- Operator "-"
	["-"]: (s) ->
		b, a = s\pop!, s\pop!
		s\push a - b

	-- Operator "*"
	["*"]: (s) ->
		b, a = s\pop!, s\pop!
		s\push a * b

	-- Operator "/"
	["/"]: (s) ->
		b, a = s\pop!, s\pop!
		s\push a / b

	-- Operator "%" (modulo)
	["%"]: (s) ->
		b, a = s\pop!, s\pop!
		s\push a % b

	-- Operator "^" (exponentiation)
	["^"]: (s) ->
		b, a = s\pop!, s\pop!
		s\push a ^ b

	-- Operator "="
	["="]: (s) ->
		b, a = s\pop!, s\pop!
		if a == b then s\push 1 else s\push 0

	-- Operator "!="
	["!="]: (s) ->
		b, a = s\pop!, s\pop!
		if a != b then s\push 1 else s\push 0

	-- Operator "<"
	["<"]: (s) ->
		b, a = s\pop!, s\pop!
		if a < b then s\push 1 else s\push 0

	-- Operator "<="
	["<="]: (s) ->
		b, a = s\pop!, s\pop!
		if a <= b then s\push 1 else s\push 0

	-- Operator ">"
	[">"]: (s) ->
		b, a = s\pop!, s\pop!
		if a > b then s\push 1 else s\push 0

	-- Operator ">="
	[">="]: (s) ->
		b, a = s\pop!, s\pop!
		if a >= b then s\push 1 else s\push 0

	abs: (s) -> s\push math.abs s\pop!
	ceil: (s) -> s\push math.ceil s\pop!
	floor: (s) -> s\push math.floor s\pop!
	pi: (s) -> s\push math.pi
	e: (s) -> s\push math.exp 1
	-- Base e logarithm
	ln: (s) -> s\push math.log s\pop!
	-- Base 10 logarithm
	log: (s) -> s\push math.log10 s\pop!
	-- Base 2 logarithm
	log2: (s) -> s\push (math.log10 s\pop!) / (math.log10 2)
	min: (s) -> s\push math.min s\pop!, s\pop!
	max: (s) -> s\push math.max s\pop!, s\pop!
	-- Duplicate top of stack
	dup: (s) -> s\push s\top!
	-- Discard top of stack
	drop: (s) -> s\pop!
	-- Discard element below top of stack
	nip: (s) ->
		b, a = s\pop!, s\pop!
		s\push b
	-- Discard entire stack
	clear: (s) -> while not s\isempty! do s\pop!
	-- Print top of stack
	print: (s) -> io.write (tostring s\top!), "\n"
	-- Print and remove top of stack
	["."]: (s) -> io.write (tostring s\pop!), "\n"
	-- Swap topmost elements
	swap: (s) ->
		b, a = s\pop!, s\pop!
		s\push b
		s\push a
	-- Duplicate element below top of stack
	-- 'a b over' is equivalent to 'a b a'
	over: (s) ->
		b, a = s\pop!, s\pop!
		s\push a
		s\push b
		s\push a
	-- Rotate top three elements
	-- 'a b c rot' is equivalent to 'b c a'
	rot: (s) ->
		c = s\pop!
		words.swap s
		s\push c
		words.swap s
	-- Print newline
	cr: -> io.write "\n"
	-- Number of elements of data stack
	elems: (s) -> s\push #s.elems
	-- Push data onto stack
	__push: (s, d) -> s\push d
	-- Conditional branch: branch on false
	__branch: (s) -> if s\pop! == 0 then true else false
	-- Conditional branch: branch on true
	-- TODO

	--------------------------------------------------------------------------
	-- Combinators
	--------------------------------------------------------------------------

	-- Apply quotation f n times
	times: (s) ->
		f, n = s\pop!, s\pop!
		for i = 1, n do f s

	-- Apply quotation f to x and put x back on top of the stack
	keep: (s) ->
		f, x = s\pop!, s\top!
		f s
		s\push x

	-- Apply quotation f to the element below the top of the stack
	dip: (s) ->
		f, x = s\pop!, s\pop!
		f s
		s\push x

	-- Cleave combinator: Apply quotations f and g to x
	bi: (s) ->
		g = s\pop!
		words.keep s
		g s

	-- Spread combinator: Apply quotations f to x and g to y
	["bi*"]: (s) ->
		g = s\pop!
		words.dip s
		g s

	-- Apply combinator: Apply quotation f to x and then to y
	["bi@"]: (s) ->
		f = s\top!
		words.dip s
		f s

	--------------------------------------------------------------------------
	-- Sequence operators
	--------------------------------------------------------------------------

	-- Get length of sequence
	length: (s) -> s\push #s\pop!

	-- Create sequence
	range: (s) ->
		seq = newseq!
		_step, _end, _start = s\pop!, s\pop!, s\pop!
		for i = _start, _end, _step
			seq[#seq+1] = i
		s\push seq

	-- Create sequence from n numbers on the stack
	mkseq: (s) ->
		seq = newseq!
		n = s\pop!
		for i = 1, n
			seq[#seq+1] = s\pop!
		s\push reverse seq

	-- Index into sequence
	["!!"]: (s) ->
		n, seq = s\pop!, s\pop!
		if n <= 0 or n > #seq
			raise "!!: index #{n} out of bounds"
		s\push seq[n]

	-- Apply quotation f to each value v in sequence seq
	each: (s) ->
		f, seq = s\pop!, s\pop!
		for _, v in ipairs seq
			s\push v
			f s

	-- Filter sequence
	filter: (s) ->
		fseq = newseq!
		p, seq = s\pop!, s\pop!
		for _, v in ipairs seq
			s\push v
			p s
			fseq[#fseq+1] = v if s\pop! == 1
		s\push fseq
}

builtin_words.__index = builtin_words

setmetatable words, builtin_words

{ :words }
