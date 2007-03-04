"""
Evaluate the AST into a DataSmart
"""

import ast_defines
import os, bb

# A table used by the
jump_table = [None for i in range(0,20)]

class AstDecorator:
    def __init__(self, type):
        self.type = type

    def __call__(self, function):
        global jump_table
        jump_table[self.type] = function
        function.ast_type = self.type
        return function


class EvaluateRoot(object):

    def accept(self, root, data, nodecache):
        """
        Evaluate the whole document
        """

        # We assume that base.bbclass and INHERITS have been
        # inherited already.

        # Reset status
        self.classes   = {}
        self.tasks     = []
        self.anonqueue = []
        self.handler   = []

        global jump_table

        for statement in root.statements:
            data.setVar('FILE', root.filename)
            jump_table[statement._ast_type](self, statement, data, nodecache)

        # Do some post processing by propagating vars to the
        # upper one
        if root.has_root():
            root.root.classes = dict.fromkeys( root.root.classes.keys() + root.classes.keys() )
            root.root.anonqueue+= self.anonqueue
            root.root.tasks    += self.tasks
            root.root.handler  += self.handler

    def expand(data,nodecache):
        """
        In future version only the expand could trigger
        write access to the cache.
        E.g. on inherit,include,require and immediate assignment
        """
        pass

    @AstDecorator(Ast.Assignment) 
    def visitAssignment(self, assignment, data, nodecache):
        """
        Assign to the dictionary

        Example is A = 'bla'
        """
        data.setVar(assignment.key, assignment.what)

    @AstDecorator(Ast.ImmediateAssignment)
    def visitImmediateAssignment(self, node, data, nodecache):
        node.expand(data, nodecache)
        data.setVar(node.key, data.expand(node.what, None))

    @AstDecorator(Ast.Export)
    def visitExport(self, node, data, nodecache):
        data.setVarFlag(node.key, "export", True)

    @AstDecorator(Ast.ConditionalAssignment)
    def visitConditional(self, node, data, nodecache):
        node.expand(data, nodecache)
        data.setVar(node.key, (data.getVar(node.key,False) or node.what))

    @AstDecorator(Ast.Prepend)
    def visitPrepend(self, node, data, nodecache):
        data.setVar(node.key, node.what + " " + (data.getVar(node.key,False) or ""))

    @AstDecorator(Ast.Append)
    def visitAppend(self, node, data, nodecache):
        data.setVar(node.key, (data.getVar(node.key,False) or "") + " " + node.what)

    @AstDecorator(Ast.Precat)
    def visitPrecat(self, node, data, nodecache):
        data.setVar(node.key, node.what + (data.getVar(node.key,False) or ""))

    @AstDecorator(Ast.Postcat)
    def visitPostcat(self, node, data, nodecache):
        data.setVar(node.key, (data.getVar(node.key,False) or "") + " " + node.what)

    @AstDecorator(Ast.Task)
    def visitTask(self, node, data, nodecache):
        var = "do_" + node.name
        data.setVarFlag(var, "task", True)

        if node.after:
            data.setVarFlag(var, "deps", node.after.split())
        if node.before:
            data.setVarFlag(var, "postdeps", node.before.split())
        node.root.tasks.append( var )

    @AstDecorator(Ast.Handler)
    def visitHandler(self, node, data, nodecache):
        data.setVarFlag(node.handler, "handler", 1)
        node.root.handler.append( node.handler )

    @AstDecorator(Ast.ExportFunction)
    def visitExportFunction(self, data, nodecache):
        """
        That is disguting. You can have EXPORT_FUNCTION and what this is doing
        is appending a classname to the function. But it makes fun if you inherit
        two classes...
        """
        node.get_direct_root().expand( data, nodecache )

        ### TODO FIXME

    @AstDecorator(Ast.Inherit)
    def visitInherit(self, node, data, nodecache):
        node.get_direct_root().expand( data, nodecache )
        if node.file in node.root.classes or node.file in nodecache.base_classes:
            return
            
        node.get_direct_root().classes[node.file] = 1

        inherit = data.expand(node.file, None)

        # Remember what we inherites
        ast = nodecache.parse_class( node.file, bb.which(os.environ['BBPATH'], "classes/%s.bbclass" % node.file ) )
        ast.root = node.root
        ast.eval( data, nodecache )

    @AstDecorator(Ast.Include)
    def visitInclude(self, data, nodecache):
        node.get_direct_root().expand( data, nodecache )
        bbpath = os.environ['BBPATH']
        if node.has_root():
            bbpath = "%s:%s" % (os.path.dirname(node.root.filename), bbpath)

        include = bb.which(bbpath, data.expand(node.file, None))

        try:
            ast = nodecache.parse_include(include)
            ast.eval( data, nodecache )
            bb.parse.mark_dependency(data, include)
        except Exception, e:
            print "Didn't work %s %s" % (node.file, include)

    @AstDecorator(Ast.Require)
    def visitRequire(self, data, nodecache):
        node.get_direct_root().expand( data, nodecache )
        bbpath = os.environ['BBPATH']
        if node.has_root():
            bbpath = "%s:%s" % (os.path.dirname(node.root.filename), bbpath)

        require = bb.which(bbpath, data.expand(node.file, None))

        #print "Require", node.file, require, node.root.filename
        ast = nodecache.parse_include(require)
        ast.eval( data, nodecache )
        bb.parse.mark_dependency(data, require)

    @AstDecorator(Ast.Procedure)
    def visitProcedure(self, node, data, nodecache):
        #print "Proc", self.key
        pass

    @AstDecorator(Ast.ProcedurePython)
    def visitProcPython(self, node, data, nodecache):
    
        """
        Is this anonymous at it to the queue
        """
        ### FIXME TODO transport this differently
        if node.key == "__anonymous" or node.key == "":
            node.root.anonqueue.append( node.what )
        else:
            data.setVar(node.key, node.what)
            data.setVarFlag(node.key, 'python', '1')
            

    @AstDecorator(Ast.ProcedureFakeroot)
    def eval(self, node, data, nodecache):
        data.setVar(node.key, node.what)
        data.setVarFlag(node.key, 'fakeroot', '1')

    @AstDecorator(Ast.Definition)
    def eval(self, node, data, nodecache):
        code = "def %s%s\n%s" % (node.a, node.b, node.c)
        bb.methodpool.insert_method( node.root.filename, code, node.root.filename )

