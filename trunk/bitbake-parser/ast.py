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


class AstItem():
    def __init__(self, type):
        self._ast_type = type
    
    def has_root(self):
        return hasattr(self, 'root')

    def get_direct_root(self):
        return getattr(self, 'root')

    def get_file_name(self):
        if self.has_root():
            return self.get_direct_root().file_name
        else:
            return ""

    def has_super_root(self):
        return hasattr(self, 'superroot')

    def get_super_root(self):
        "Return the toplevel node"
        return getattr(self, 'superroor')

    def expand(self, data, nodecache):
        if self.has_root():
            self.get_direct_root().expand(data, nodecache)

class Root(AstItem):
    """
    The root document
    """

    def __init__(self, filename):
        AstItem.__init__(self, Ast.Root)
        self.filename = filename
        self.statements = []
        self.base_classes = {}
        self.task_base    = []
        self.queue_base   = []
        
    def add_statement(self, statement):
        statement.root = self
        self.statements.append( statement )


    def expand(self, data, nodecache):
        """
        This will be used to fold the tree back to. E.g. due a inherit, include
        needed expand...
        """
        
class Assignment(AstItem):
    """
    An assigment like A = 'foobar'
    """
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.Assignment)
        self.key  = key
        self.what = what

class ImmediateAssignment(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.ImmediateAssignment)
        self.key   = key
        self.what  = what

class Export(AstItem):
    def __init__(self, key):
        AstItem.__init__(self, Ast.Export)
        self.key = key

class Conditional(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.ConditionalAssignment)
        self.key = key
        self.what = what

class Prepend(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.Prepend)
        self.key = key
        self.what = what

class Append(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.Append)
        self.key  = key
        self.what = what

class Precat(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.Precat)
        self.key = key
        self.what = what

class Postcat(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.Postcat)
        self.key = key
        self.what = what


class AddTask(AstItem):
    def __init__(self, name, before, after):
        AstItem.__init__(self, Ast.Task)
        self.name = name
        self.before = before
        self.after = after

class AddHandler(AstItem):
    def __init__(self, handler):
        AstItem.__init__(self, Ast.Handler)
        self.handler = handler

    def __str__(self):
        return "AddHandler: %s" % self.handler

class ExportFunction(AstItem):
    def __init__(self, function_name):
        AstItem.__init__(self, Ast.ExportFunction)
        self.function = function_name

class Inherit(AstItem):
    def __init__(self, file):
        AstItem.__init__(self, Ast.Inherit)
        self.file = file

class Include(AstItem):
    def __init__(self, file):
        AstItem.__init__(self, Ast.Include)
        self.file = file

class Require(AstItem):
    def __init__(self, file):
        AstItem.__init__(self, Ast.Require)
        self.file = file

class Proc(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.Procedure)
        self.key = key
        self.what = what

class ProcPython(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.ProcedurePython)
        self.key = key
        self.what = what

class ProcFakeroot(AstItem):
    def __init__(self, key, what):
        AstItem.__init__(self, Ast.ProcedureFakeroot)
        self.key = key
        self.what = what

class Def(AstItem):
    def __init__(self, a, b, c):
        AstItem.__init__(self, Ast.Definition)
        self.a = a
        self.b = b
        self.c = c

