"""
Evaluate the AST into a DataSmart
"""

import ast_defines

class EvaluateRoot(object):
    def eval(self, data, nodecache):
        """
        Evaluate the whole document
        """
        for statement in self.statements:
            statement.eval(data, nodecache)

        # If we are the root, do some post processing
    def expand(data,nodecache):
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
        self.get_root().expand( data, nodecache )
        print self.function

class EvaluateInherit(object):
    def eval(self, data, nodecache):
        self.get_root().expand( data, nodecache )

class EvaluateInclude(object):
    def eval(self, data, nodecache):
        self.get_root().expand( data, nodecache )

class EvaluateRequire(object):
    def eval(self, data, nodecache):
        self.get_root().expand( data, nodecache )

class EvaluateProcedure(object):
    def eval(self, data, nodecache):
        pass

class EvaluateProcedurePython(object):
    def eval(self, data, nodecache):
        pass

class EvaluateProcedureFakeroot(object):
    def eval(self, data, nodecache):
        pass

class EvaluateDefinition(object):
    def eval(self, data, nodecache):
        pass


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
