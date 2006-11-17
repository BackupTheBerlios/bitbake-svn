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

class EvaluateAssignment(object):
    def eval(self, data, nodecache):
        """
        Assign to the dictionary

        Example is A = 'bla'
        """
        data.setVar(self.key, self.what)

class EvaluateImmediateAssignment(object):
    def eval(self, data, nodecache):
        if hasattr(self, 'root'):
            self.root.expand(data, nodecache)
        data.setVar(self.key, data.expand(self.what, None))

class EvaluateExport(object):
    def eval(self, data, nodecache):
        data.setVarFlag(self.key, "export", True)

class EvaluateConditionalAssigment(object):
    def eval(self, data, nodecache):
        if hasattr(self, 'root'):
            self.root.expand(data, nodecache)

class EvaluatePrepend(object):
    def eval(self, data, nodecache):
        pass

class EvaluateAppend(object):
    def eval(self, data, nodecache):
        pass

class EvaluatePrecat(object):
    def eval(self, data, nodecache):
        pass

class EvaluatePostcat(object):
    def eval(self, data, nodecache):
        pass

class EvaluateTask(object):
    def eval(self, data, nodecache):
        pass

class EvaluateHandler(object):
    def eval(self, data, nodecache):
        pass

class EvaluateExportFunction(object):
    def eval(self, data, nodecache):
        pass

class EvaluateInherit(object):
    def eval(self, data, nodecache):
        pass

class EvaluateInclude(object):
    def eval(self, data, nodecache):
        pass

class EvaluateRequire(object):
    def eval(self, data, nodecache):
        pass

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
