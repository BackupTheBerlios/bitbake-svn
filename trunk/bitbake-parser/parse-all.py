import bitbakec
import bb
import os

asts = []

for root, dirs, files in os.walk('/space/hacking/embedded/oe/org.openembedded.dev/'):
    for file in files:
        (r2, ext) = os.path.splitext(file)
        if not ext in ['.inc', '.bb', '.conf', '.bbclass']:
            continue
        
        path = os.path.join(root, file)
        #print "Parsing %s" % path
        ast = bitbakec.parsefile(path,False)
        asts.append( ast )
        try:
            ast.eval( bb.data.init(), None )
        except:
            pass

import time
time.sleep( 60000 )
