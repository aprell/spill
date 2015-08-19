import concat, raise from require "util"

class Stack
	new: => @elems = {}
	push: (val) => @elems[#@elems+1] = val
	pop: => table.remove(@elems) or raise "pop: empty stack"
	top: => @elems[#@elems] or raise "top: empty stack"
	isempty: => #@elems == 0
	__tostring: => "[#{concat @elems, ", "}]"

class Queue extends Stack
	enq: (val) => @push val
	deq: => table.remove @elems, 1
	front: => @elems[1]

{ :Stack }
