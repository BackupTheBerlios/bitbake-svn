import bitbakec
import bb
import os, sys
import nodecache

asts = []

bb.msg.set_verbose( False )
bb.msg.set_debug_level( 0 )
bb.msg.set_debug_domains([])

cache = nodecache.NodeCache(bitbakec.parsefile)

# Read the Configuration
my_init = bb.data.init()
bb.data.inheritFromOS(my_init)
my_init.setVar('TOPDIR', os.getcwd() )
conf = bitbakec.parsefile(bb.which(os.environ['BBPATH'], "conf/bitbake.conf"), True)
conf.eval( my_init, cache )


# micro optimisation INHERIT the bases once...
import ast
require = ast.Inherit("none")
inherits = (my_init.getVar('INHERIT', True) or "").split()
inherits.insert(0, "base")
for inherit in inherits:
    require.file = inherit
    require.eval( my_init, cache )

# Finish up one file!
def finish_up(the_data):
    """
    This takes +*LOOOOONG* seconds... fix it
    """
    bb.data.expandKeys(the_data)
    bb.data.update_data(the_data)

    anonqueue = bb.data.getVar("__anonqueue", the_data, 1) or []
    for anon in anonqueue:
        bb.data.setVar("__anonfunc", anon["content"], the_data)
        bb.data.setVarFlags("__anonfunc", anon["flags"], the_data)
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
    bb.data.delVar("__anonqueue", the_data)
    bb.data.delVar("__anonfunc", the_data)
    #set_additional_vars(fn, d, include)
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
        asts.append( ast )
        try:
            data = my_init.createCopy()
            ast.classes = inherits
            ast.eval( data, cache )
            finish_up( data )
        except Exception, e:
            print "Error eval", e
        except:
            pass

import time
#time.sleep( 60000 )
