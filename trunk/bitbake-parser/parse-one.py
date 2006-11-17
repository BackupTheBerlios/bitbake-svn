import bitbakec
import os,sys

asts = []
asts.append( bitbakec.parsefile(sys.argv[1],False) )

for statement in asts[0].statements:
    print statement

import time
time.sleep( 60000 )
