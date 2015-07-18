reverse = (list) ->
	for i = 1, math.floor #list/2
		list[i], list[#list-i+1] = list[#list-i+1], list[i]
	return list

concat = (list, sep = " ") ->
	s = ""
	for i = 1, #list
		s ..= tostring list[i]
		s ..= sep unless i == #list
	return s

newseq = -> setmetatable {}, {__tostring: (seq) -> "{ #{concat seq} }"}

raise = (err_msg) ->
	error setmetatable {reason: err_msg}, {__tostring: (err) -> err.reason}

{ :reverse, :concat, :newseq, :raise }
