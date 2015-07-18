import concat from require "util"

class Stack
	new: => @elems = {}
	push: (val) => @elems[#@elems+1] = val
	pop: => table.remove(@elems)
	top: => @elems[#@elems]
	isempty: => #@elems == 0
	dump: => "[#{concat @elems, ", "}]"

class Queue extends Stack
	enq: (val) => @push val
	deq: => table.remove @elems, 1
	front: => @elems[1]

{ :Stack, :Queue }
