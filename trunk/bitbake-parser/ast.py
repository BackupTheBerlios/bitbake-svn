"""
    Do not use or send me a postcard

    AbstractSyntaxTree for the BitBake parser

    The Root is the Root class where all statements
    are inserted to. eval will evaluate these statements
    in order

        Root
        /      \
    Statement   Next One
    /  \        /  \
                    Next One


    How to optimize it:
        Keep prepends and append in an array [] only evaluate it
        when we have immediate assign or need to expand (e.g.
        on includin other files).


    Each child has a pointer to its Root, each Root has a pointer
    to the other Root.

"""

class Root:
    """
    The root document
    """

    def __init__(self, filename):
        self.filename = filename
        self.statements = []
        self.root = None

    def eval(self, data, nodecache):
        """
        Evaluate the whole document
        """
        for statement in self.statements:
            statement.eval(data, nodecache)

    def add_statement(self, statement):
        statement.root = self
        self.statements.append( statement )


    def expand(self, data, nodecache):
        """
        This will be used to fold the tree back to. E.g. due a inherit, include
        needed expand...
        """
        

class Assignment:
    """
    An assigment like A = 'foobar'
    """
    def __init__(self, key, what):
        self.key  = key
        self.what = what

    def eval(self, data, nodecache):
        """
        Assign to the dictionary

        Example is A = 'bla'
        """
        data.setVar(self.key, self.what)

class ImmediateAssignment:
    def __init__(self, key, what):
        self.key   = key
        self.what  = what

    def eval(self, data, nodecache):
        if hasattr(self, 'root'):
            self.root.expand(data, nodecache)
        data.setVar(self.key, data.expand(self.what, None))

class Export:
    def __init__(self, key):
        self.key = key

    def eval(self, data, nodecache):
        data.setVarFlag(self.key, "export", True)


class Conditional:
    def __init__(self, key, what):
        self.key = key
        self.what = what

    def eval(self, data, nodecache):
        if hasattr(self, 'root'):
            self.root.expand(data, nodecache)
        

class Prepend:
    def __init__(self, key, what):
        self.key = key
        self.what = what

    def eval(self, data, nodecache):
        pass

class Append:
    def __init__(self, key, what):
        self.key  = key
        self.what = what

    def eval(self, data, nodecache):
        pass

class Precat:
    def __init__(self, key, what):
        self.key = key
        self.what = what

    def eval(self, data, nodecache):
        pass

class Postcat:
    def __init__(self, key, what):
        self.key = key
        self.what = what

    def eval(self, data, nodecache):
        pass

class AddTask:
    def __init__(self, name, before, after):
        self.name = name
        self.before = before
        self.after = after

    def eval(self, data, nodecache):
        pass


class AddHandler:
    def __init__(self, handler):
        self.handler = handler

    def eval(self, data, nodecache):
        pass

    def __str__(self):
        return "AddHandler: %s" % self.handler

class ExportFunction:
    def __init__(self, function_name):
        self.function = function_name

    def eval(self, data, nodecache):
        pass

class Inherit:
    def __init__(self, file):
        self.file = file
    def eval(self, data, nodecache):
        pass

class Include:
    def __init__(self, file):
        self.file = file

    def eval(self, data, nodecache):
        pass


class Require:
    def __init__(self, file):
        self.file = file

    def eval(self, data, nodecache):
        pass


class Proc:
    def __init__(self, key, what):
        self.key = key
        self.what = what
    def eval(self, data, nodecache):
        pass

class ProcPython:
    def __init__(self, key, what):
        self.key = key
        self.what = what
    def eval(self, data, nodecache):
        pass

class ProcFakeroot:
    def __init__(self, key, what):
        self.key = key
        self.what = what

    def eval(self, data, nodecache):
        pass

class Def:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def eval(self, data, nodecache):
        pass
