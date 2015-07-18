import concat, raise from require "util"

class Stack
	new: => @elems = {}
	push: (val) => @elems[#@elems+1] = val
	pop: =>
		if @isempty! then raise "pop: stack empty"
		table.remove(@elems)
	top: =>
		if @isempty! then raise "top: stack empty"
		@elems[#@elems]
	isempty: => #@elems == 0
	dump: => "[#{concat @elems, ", "}]"

class Queue extends Stack
	enq: (val) => @push val
	deq: => table.remove @elems, 1
	front: => @elems[1]

{ :Stack }
