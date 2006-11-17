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

from ast_defines import Ast


def mixing_factory(ast_name):
    """
    Create a  class which implements the appropriate evaluation method
    """
    import evaluator_data
    return evaluator_data.create(ast_name)

class Root(mixing_factory(Ast.Root)):
    """
    The root document
    """

    def __init__(self, filename):
        self.filename = filename
        self.statements = []
        self.root = None

    def add_statement(self, statement):
        statement.root = self
        self.statements.append( statement )


    def expand(self, data, nodecache):
        """
        This will be used to fold the tree back to. E.g. due a inherit, include
        needed expand...
        """
        
class Assignment(mixing_factory(Ast.Assignment)):
    """
    An assigment like A = 'foobar'
    """
    def __init__(self, key, what):
        self.key  = key
        self.what = what

class ImmediateAssignment(mixing_factory(Ast.ImmediateAssignment)):
    def __init__(self, key, what):
        self.key   = key
        self.what  = what

class Export(mixing_factory(Ast.Export)):
    def __init__(self, key):
        self.key = key

class Conditional(mixing_factory(Ast.ConditionalAssignment)):
    def __init__(self, key, what):
        self.key = key
        self.what = what

class Prepend(mixing_factory(Ast.Prepend)):
    def __init__(self, key, what):
        self.key = key
        self.what = what

class Append(mixing_factory(Ast.Append)):
    def __init__(self, key, what):
        self.key  = key
        self.what = what

class Precat(mixing_factory(Ast.Precat)):
    def __init__(self, key, what):
        self.key = key
        self.what = what

class Postcat(mixing_factory(Ast.Postcat)):
    def __init__(self, key, what):
        self.key = key
        self.what = what


class AddTask(mixing_factory(Ast.Task)):
    def __init__(self, name, before, after):
        self.name = name
        self.before = before
        self.after = after

class AddHandler(mixing_factory(Ast.Handler)):
    def __init__(self, handler):
        self.handler = handler

    def __str__(self):
        return "AddHandler: %s" % self.handler

class ExportFunction(mixing_factory(Ast.ExportFunction)):
    def __init__(self, function_name):
        self.function = function_name

class Inherit(mixing_factory(Ast.Inherit)):
    def __init__(self, file):
        self.file = file

class Include(mixing_factory(Ast.Include)):
    def __init__(self, file):
        self.file = file

class Require(mixing_factory(Ast.Require)):
    def __init__(self, file):
        self.file = file

class Proc(mixing_factory(Ast.Procedure)):
    def __init__(self, key, what):
        self.key = key
        self.what = what

class ProcPython(mixing_factory(Ast.ProcedurePython)):
    def __init__(self, key, what):
        self.key = key
        self.what = what

class ProcFakeroot(mixing_factory(Ast.ProcedureFakeroot)):
    def __init__(self, key, what):
        self.key = key
        self.what = what

class Def(mixing_factory(Ast.Definition)):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

