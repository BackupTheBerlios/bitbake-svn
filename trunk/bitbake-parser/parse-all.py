import bitbakec
import bb
import os, sys
import nodecache

asts = []

bb.msg.set_verbose( False )
bb.msg.set_debug_level( 0 )
bb.msg.set_debug_domains([])


def main():
    cache = nodecache.NodeCache(bitbakec.parsefile)
    # Read the Configuration
    my_init = bb.data.init()
    bb.data.inheritFromOS(my_init)
    my_init.setVar('TOPDIR', os.getcwd() )
    conf = bitbakec.parsefile(bb.which(os.environ['BBPATH'], "conf/bitbake.conf"), True)
    conf.eval( my_init, cache )


    # micro optimisation INHERIT the bases once...
    import ast
    root = ast.Root("none")
    inherits = (my_init.getVar('INHERIT', True) or "").split()
    inherits.insert(0, "base")
    for inherit in inherits:
        print "Inheriting %s" % inherit
        root.add_statement( ast.Inherit( inherit ) )

    root.eval( my_init, cache )
    base_classes = root.classes
    print base_classes
    #sys.exit(-1)
    # Initialize the fetcher stuff
    def set_additional_vars(the_data):
        """Deduce rest of variables, e.g. ${A} out of ${SRC_URI}"""

        src_uri = bb.data.getVar('SRC_URI', the_data)
        if not src_uri:
            return
        src_uri = bb.data.expand(src_uri, the_data)

        a = bb.data.getVar('A', the_data)
        if a:
            a = bb.data.expand(a, the_data).split()
        else:
            a = []

        from bb import fetch
        try:
            fetch.init(src_uri.split(), the_data)
        except fetch.NoMethodError:
            pass
        except bb.MalformedUrl,e:
            raise bb.parse.ParseError("Unable to generate local paths for SRC_URI due to malformed uri: %s" % e)

        a += fetch.localpaths(the_data)
        del fetch
        bb.data.setVar('A', " ".join(a), the_data)

    # Finish up one file!
    def finish_up(ast,the_data):
        """
        This takes +*LOOOOONG* seconds... fix it
        """
        bb.data.expandKeys(the_data)
        bb.data.update_data(the_data)


        flag = {'python' : 1, 'func' : 1}
        for anon in ast.anonqueue:
            bb.data.setVar("__anonfunc"     , anon, the_data)
            bb.data.setVarFlags("__anonfunc", flag, the_data)
            try: 
                t = bb.data.getVar('T', the_data)
                bb.data.setVar('T', '${TMPDIR}/', the_data)
                bb.build.exec_func("__anonfunc", the_data)
                bb.data.delVar('T', the_data)
                if t:
                    bb.data.setVar('T', t, the_data)
            except Exception, e:
                #bb.msg.debug(1, bb.msg.domain.Parsing, "executing anonymous function: %s" % e)
                raise
        bb.data.delVar("__anonfunc", the_data)
        set_additional_vars(the_data)
        bb.data.update_data(the_data)  

    # Parse all functions
    for root, dirs, files in os.walk('/space/hacking/embedded/oe/org.openembedded.dev/'):
        for file in files:
            (r2, ext) = os.path.splitext(file)
            if not ext in ['.bb' ]:
                continue
        
            path = os.path.join(root, file)
            #print "Parsing %s" % path
            ast = bitbakec.parsefile(path,False)
            if not ast:
                continue
            try:
                data = my_init.createCopy()
                ast.base_classes = base_classes
                ast.eval( data, cache )
                finish_up( ast, data )
            except Exception, e:
                print "Error eval", e
            except:
                pass


#import cProfile
#cProfile.run("main()")
main()
import time
#time.sleep( 60000 )
