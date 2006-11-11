# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
import ast
import bb.parse

cdef extern from "stdio.h":
    ctypedef int FILE
    FILE *fopen(char*, char*)
    int fclose(FILE *fp)

cdef extern from "string.h":
    int strlen(char*)

cdef extern from "lexerc.h":
    ctypedef struct lex_t:
        void* parser
        void* scanner
        FILE* file
        char* name
        void* tree
        int config
        int error
        int lineno

    cdef extern int parse(FILE*, char*, object, int)

def parsefile(object file, object config):
    #print "parsefile: 1", file, data

    # Open the file
    cdef FILE* f

    f = fopen(file, "r")
    #print "parsefile: 2 opening file"
    if (f == NULL):
        raise IOError("No such file %s" % file)

    #print "parsefile: 3 parse"
    root = ast.Root(file)
    ret = parse(f, file, root, config)

    # Close the file
    fclose(f)

    if ret == 0:
        #raise bb.parse.ParseError(), file
        print "ParseError"

    return root



cdef public void e_assign(lex_t* container, char* key, char* what):
    #print "e_assign", key, what
    if what == NULL:
        print "FUTURE Warning empty string: use \"\""
        what = ""

    tree = <object>container.tree
    tree.add_statement( ast.Assignment( key, what ) )

cdef public void e_export(lex_t* c, char* what):
    #print "e_export", what
    #exp:
    # bb.data.setVarFlag(key, "export", 1, data)
    tree = <object>c.tree
    tree.add_statement( ast.Export( what ) )

cdef public void e_immediate(lex_t* c, char* key, char* what):
    #print "e_immediate", key, what
    #colon:
    # val = bb.data.expand(groupd["value"], data)
    tree = <object>c.tree
    tree.add_statement( ast.ImmediateAssignment( key, what ) )

cdef public void e_cond(lex_t* c, char* key, char* what):
    #print "e_cond", key, what
    #ques:
    # val = bb.data.getVar(key, data)
    # if val == None:    
    #    val = groupd["value"]
    if what == NULL:
        print "FUTURE warning: Use \"\" for", key
        what = ""

    tree = <object>c.tree
    tree.add_statement( ast.Conditional( key, what ) )

cdef public void e_prepend(lex_t* c, char* key, char* what):
    #print "e_prepend", key, what
    #prepend:
    # val = "%s %s" % (groupd["value"], (bb.data.getVar(key, data) or ""))
    tree = <object>c.tree
    tree.add_statement( ast.Prepend( key, what ) )

cdef public void e_append(lex_t* c, char* key, char* what):
    #print "e_append", key, what
    #append:
    # val = "%s %s" % ((bb.data.getVar(key, data) or ""), groupd["value"])
    tree = <object>c.tree
    tree.add_statement( ast.Append( key, what ) )

cdef public void e_precat(lex_t* c, char* key, char* what):
    #print "e_precat", key, what
    #predot:
    # val = "%s%s" % (groupd["value"], (bb.data.getVar(key, data) or ""))
    tree = <object>c.tree
    tree.add_statement( ast.Precat( key, what ) )

cdef public void e_postcat(lex_t* c, char* key, char* what):
    #print "e_postcat", key, what
    #postdot:
    # val = "%s%s" % ((bb.data.getVar(key, data) or ""), groupd["value"])
    tree = <object>c.tree
    tree.add_statement( ast.Postcat( key, what ) )

cdef public int e_addtask(lex_t* c, char* name, char* before, char* after) except -1:
    #print "e_addtask", name
    # func = m.group("func")
    # before = m.group("before")
    # after = m.group("after")
    # if func is None:
    #     return
    # var = "do_" + func
    #
    # data.setVarFlag(var, "task", 1, d)
    #
    # if after is not None:
    # #  set up deps for function
    #     data.setVarFlag(var, "deps", after.split(), d)
    # if before is not None:
    # #   set up things that depend on this func
    #     data.setVarFlag(var, "postdeps", before.split(), d)
    # return

    if c.config == 1:
        raise bb.parse.ParseError("No tasks allowed in config files")
        return -1

    tree = <object>c.tree
    if before == NULL:
        before = ""
    if after == NULL:
        after = ""

    tree.add_statement( ast.AddTask( name, before, after ) )

    return 0

cdef public int e_addhandler(lex_t* c, char* h) except -1:
    #print "e_addhandler", h
    # data.setVarFlag(h, "handler", 1, d)
    if c.config == 1:
        raise bb.parse.ParseError("No handlers allowed in config files")
        return -1

    tree = <object>c.tree
    tree.add_statement( ast.AddHandler( h ) )
    return 0

cdef public int e_export_func(lex_t* c, char* function) except -1:
    #print "e_export_func", function
    if c.config == 1:
        raise bb.parse.ParseError("No functions allowed in config files")
        return -1

    tree = <object>c.tree
    tree.add_statement( ast.ExportFunction( function ) )
    return 0

cdef public int e_inherit(lex_t* c, char* file) except -1:
    #print "e_inherit", file

    if c.config == 1:
        raise bb.parse.ParseError("No inherits allowed in config files")
        return -1

    tree = <object>c.tree
    tree.add_statement( ast.Inherit( file ) )
    

    return 0

cdef public void e_include(lex_t* c, char* file):
    tree = <object>c.tree
    tree.add_statement( ast.Include( file ) )


cdef public int e_require(lex_t* c, char* file) except -1:
    #print "e_require", file
    tree = <object>c.tree
    tree.add_statement( ast.Require( file ) )
    return 0

cdef public int e_proc(lex_t* c, char* key, char* what) except -1:
    #print "e_proc", key, what
    if c.config == 1:
        raise bb.parse.ParseError("No inherits allowed in config files")
        return -1

    if key == NULL:
        key = ""
    if what == NULL:
        what = ""

    tree = <object>c.tree
    tree.add_statement( ast.Proc( key, what ) )
    return 0

cdef public int e_proc_python(lex_t* c, char* key, char* what) except -1:
    #print "e_proc_python"
    if c.config == 1:
        raise bb.parse.ParseError("No pythin allowed in config files")
        return -1

    tree = <object>c.tree
    if key == NULL:
        key = ""
    if what == NULL:
        what = ""

    tree.add_statement( ast.ProcPython( key, what ) )

    return 0

cdef public int e_proc_fakeroot(lex_t* c, char* key, char* what) except -1:
    #print "e_fakeroot", key, what

    if c.config == 1:
        raise bb.parse.ParseError("No fakeroot allowed in config files")
        return -1

    tree = <object>c.tree
    tree.add_statement( ast.ProcFakeroot( key, what ) )

    return 0

cdef public int e_def(lex_t* c, char* a, char* b, char* d) except -1:
    #print "e_def", a, b, d

    if c.config == 1:
        raise bb.parse.ParseError("No defs allowed in config files")
        return -1

    tree = <object>c.tree
    tree.add_statement( ast.Def( a, b, d ) )

    return 0

cdef public int e_parse_error(lex_t* c):
    print "e_parse_error", c.name, "line:", c.lineno, "parse:", c.error

    if c.error == 0:
        c.error  = 1010
    return 0

