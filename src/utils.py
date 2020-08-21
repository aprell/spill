#reverse = (list) ->
#	for i = 1, math.floor #list/2
#		list[i], list[#list-i+1] = list[#list-i+1], list[i]
#	return list

def reverse(lst):
    lst.reverse()
    return lst

#concat = (list, sep = " ") ->
#	s = ""
#	for i = 1, #list
#		s ..= tostring list[i]
#		s ..= sep unless i == #list
#	return s

def concat(lst, sep=" "):
    return sep.join(str(i) for i in lst)

#newseq = -> setmetatable {}, {__tostring: (seq) -> "{ #{concat seq} }"}

class Sequence:
    def __init__(self, lst=[]):
        self.seq = lst

    def __iter__(self):
        return iter(self.seq)

    def __len__(self):
        return len(self.seq)

    def __str__(self):
        return f"{{ {concat(self.seq)} }}"

    def append(self, value):
        self.seq.append(value)

    def reverse(self):
        self.seq.reverse()

#raise = (err_msg) ->
#	error setmetatable {reason: err_msg}, {__tostring: (err) -> err.reason}
#
#{ :reverse, :concat, :newseq, :raise }
