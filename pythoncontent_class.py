def srepr(obj, tab):
    try:
        return obj.lines_repr(tab)
    except:
        return repr(obj)

class mylist(list):
    def __init__(self, l):
        list.__init__(self, l)

    def __repr__(self):
        return self.lines_repr(0)

    def lines_repr(self, tab):
        return "mylist([\n%s\n%s])" % ('\n'.join( "%s%s,"%('    '*(tab+1), srepr(item, tab+1)) for item in self ), '    '*tab)


class mydict(dict):
    def __init__(self, d):
        dict.__init__(self, **d)

    def __repr__(self):
        return self.lines_repr(0)

    def lines_repr(self, tab):
        return "mydict({\n%s\n%s})" % ('\n'.join( "%s'%s':%s,"%('    '*(tab+1), key, srepr(value, tab+1)) for (key, value) in self.items() ), '    '*tab)


class pySerie(dict):
    def __init__(self, d):
        dict.__init__(self, **d)

    def __repr__(self):
        return "pySerie({\n%s\n        })" % '\n'.join( "        '%s':%s,"%(key, repr(value)) for (key, value) in self.items() )


class pyContent(dict):
    def __init__(self, d):
        dict.__init__(self, **d)

    def __repr__(self):
        return "pyContent({\n%s\n    })" % '\n'.join( sorted(["    '%s':%s,"%(key, repr(value)) for (key, value) in self.items() ]))


with open('pythoncontent.py', 'r') as f:
    obj = eval(f.read())

def save():
    repr(obj)
    with open('pythoncontent.py', 'w') as f:
        f.write(repr(obj))