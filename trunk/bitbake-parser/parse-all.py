import bitbakec
import bb
import os, sys
import nodecache

asts = []

cache = nodecache.NodeCache(bitbakec.parsefile)

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
            ast.classes = inherits
            ast.eval( my_init.createCopy(), cache )
        except Exception, e:
            print "Error eval", e
        except:
            pass

import time
#time.sleep( 60000 )
