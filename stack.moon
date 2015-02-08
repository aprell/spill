class Stack
	new: => @elems = {}
	push: (val) => @elems[#@elems+1] = val
	pop: => table.remove(@elems)
	top: => @elems[#@elems]
	isempty: => #@elems == 0
	dump: =>
		s = "["
		for i = 1, #@elems
			s ..= tostring @elems[i]
			s ..= ", " unless i == #@elems
		s ..= "]\n"
		return s

class Queue extends Stack
	enq: (val) => @push val
	deq: => table.remove @elems, 1
	front: => @elems[1]

{ :Stack, :Queue }
