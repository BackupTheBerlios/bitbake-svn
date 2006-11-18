"""
Cache the result of include files, and bitbake classes
"""


class NodeCache:
    """
    Cache to allow linking the BitBake includes, classes and
    requirements.

    The secret of the class will be how we cache
    """
    def __init__(self,parse_method):
        self.parse_method = parse_method
        self.includes     = {}
        self.classes      = {}
        self.base_classes = {}


    def parse_class(self, classname, classfile):
        """
        Parse a class or use a cached one
        """
        try:
            return self.classes[classname]
        except KeyError:
            try:
                print "inheriting class %s %s" % (classname, classfile)
                ast = self.parse_method(classfile,False)
                if ast:
                    self.classes[classname] = ast
                    return ast
                raise Exception("Can not inherit")
            except Exception, e:
                print e
                raise Exception("Class not found/usable %s" % classname)

    def parse_include(self, includename):
        try:
            return self.includes[includename]
        except KeyError:
            try:
                ast = self.parse_method(includename, '.conf' == includename[-5] )
                if ast:
                    self.includes[includename] = ast
                    return ast
            except:
                raise Exception("Include not found/usable %s" % includename)

