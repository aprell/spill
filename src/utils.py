def reverse(lst):
    lst.reverse()
    return lst

def concat(lst, sep=" "):
    return sep.join(str(i) for i in lst)

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
