"""
Evaluate the AST into a DataSmart
"""

import ast_defines
import os, bb

class EvaluateRoot(object):
    def eval(self, data, nodecache):
        """
        Evaluate the whole document
        """

        # We assume that base.bbclass and INHERITS have been
        # inherited already.

        for statement in self.statements:
            data.setVar('FILE', self.filename)
            statement.eval(data, nodecache)

        # If we are the root, do some post processing
    def expand(data,nodecache):
        """
        In future version only the expand could trigger
        write access to the cache.
        E.g. on inherit,include,require and immediate assignment
        """
        pass

class EvaluateAssignment(object):
    def eval(self, data, nodecache):
        """
        Assign to the dictionary

        Example is A = 'bla'
        """
        data.setVar(self.key, self.what)

class EvaluateImmediateAssignment(object):
    def eval(self, data, nodecache):
        self.expand(data, nodecache)
        data.setVar(self.key, data.expand(self.what, None))

class EvaluateExport(object):
    def eval(self, data, nodecache):
        data.setVarFlag(self.key, "export", True)

class EvaluateConditionalAssigment(object):
    def eval(self, data, nodecache):
        self.expand(data, nodecache)
        data.setVar(self.key, (data.getVar(self.key,False) or self.what))

class EvaluatePrepend(object):
    def eval(self, data, nodecache):
        data.setVar(self.key, self.what + " " + (data.getVar(self.key,False) or ""))

class EvaluateAppend(object):
    def eval(self, data, nodecache):
        data.setVar(self.key, (data.getVar(self.key,False) or "") + " " + self.what)

class EvaluatePrecat(object):
    def eval(self, data, nodecache):
        data.setVar(self.key, self.what + (data.getVar(self.key,False) or ""))

class EvaluatePostcat(object):
    def eval(self, data, nodecache):
        data.setVar(self.key, (data.getVar(self.key,False) or "") + " " + self.what)

class EvaluateTask(object):
    def eval(self, data, nodecache):
        var = "do_" + self.name
        data.setVarFlag(var, "task", True)

        if self.after:
            data.setVarFlag(var, "deps", self.after.split())
        if self.before:
            data.setVarFlag(var, "postdeps", self.before.split())

class EvaluateHandler(object):
    def eval(self, data, nodecache):
        data.setVarFlag(self.handler, "handler", 1)

class EvaluateExportFunction(object):
    def eval(self, data, nodecache):
        """
        That is disguting. You can have EXPORT_FUNCTION and what this is doing
        is appending a classname to the function. But it makes fun if you inherit
        two classes...
        """
        self.get_direct_root().expand( data, nodecache )

        ### TODO FIXME

class EvaluateInherit(object):
    def eval(self, data, nodecache):
        if self.has_root():
            self.get_direct_root().expand( data, nodecache )
        inherit = data.expand(self.file, None)

        # Remember what we inherites
        if self.has_root():
            self.get_direct_root().classes.append( self.file )
        ast = nodecache.parse_class( self.file, bb.which(os.environ['BBPATH'], "classes/%s.bbclass" % self.file ) )
        ast.eval( data, nodecache )

class EvaluateInclude(object):
    def eval(self, data, nodecache):
        self.get_direct_root().expand( data, nodecache )
        bbpath = os.environ['BBPATH']
        if self.has_root():
            bbpath = "%s:%s" % (os.path.dirname(self.root.filename), bbpath)

        include = bb.which(bbpath, data.expand(self.file, None))

        try:
            ast = nodecache.parse_include(include)
            ast.eval( data, nodecache )
            bb.parse.mark_dependency(data, include)
        except Exception, e:
            print "Didn't work %s %s" % (self.file, include)

class EvaluateRequire(object):
    def eval(self, data, nodecache):
        self.get_direct_root().expand( data, nodecache )
        bbpath = os.environ['BBPATH']
        if self.has_root():
            bbpath = "%s:%s" % (os.path.dirname(self.root.filename), bbpath)

        require = bb.which(bbpath, data.expand(self.file, None))

        #print "Require", self.file, require, self.root.filename
        ast = nodecache.parse_include(require)
        ast.eval( data, nodecache )
        bb.parse.mark_dependency(data, require)

class EvaluateProcedure(object):
    def eval(self, data, nodecache):
        #print "Proc", self.key
        pass

class EvaluateProcedurePython(object):
    def eval(self, data, nodecache):
        """
        Is this anonymous at it to the queue
        """
        ### FIXME TODO transport this differently
        if self.key == "__anonymous" or self.key == "":
            anonqueue = data.getVar('__anonqueue', False) or []
            anonqueue.append( {'content' : self.what, 'flags' : { 'python' : 1, 'func' : 1}} )
            data.setVar('__anonqueue', anonqueue )
        else:
            data.setVar(self.key, self.what)
            data.setVarFlag(self.key, 'python', '1')
            

class EvaluateProcedureFakeroot(object):
    def eval(self, data, nodecache):
        data.setVar(self.key, self.what)
        data.setVarFlag(self.key, 'fakeroot', '1')

class EvaluateDefinition(object):
    def eval(self, data, nodecache):
        code = "def %s%s\n%s" % (self.a, self.b, self.c)
        bb.methodpool.insert_method( self.root.filename, code, self.root.filename )


# this needs to match ast_defines.Ast
node_list = [
    None,
    EvaluateRoot,
    EvaluateAssignment,
    EvaluateImmediateAssignment,
    EvaluateExport,
    EvaluateConditionalAssigment,
    EvaluatePrepend,
    EvaluateAppend,
    EvaluatePrecat,
    EvaluatePostcat,
    EvaluateTask,
    EvaluateHandler,
    EvaluateExportFunction,
    EvaluateInherit,
    EvaluateInclude,
    EvaluateRequire,
    EvaluateProcedure,
    EvaluateProcedurePython,
    EvaluateProcedureFakeroot,
    EvaluateDefinition
]


def create(ast_name):
    return node_list[ast_name]
