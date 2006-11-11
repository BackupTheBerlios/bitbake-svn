import bitbakec
import os

for root, dirs, files in os.walk('/space/hacking/embedded/oe/org.openembedded.dev/'):
    for file in files:
        path = os.path.join(root, file)
        print "Parsing %s" % path
        bitbakec.parsefile(path,False)


