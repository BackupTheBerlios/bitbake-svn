"""
Cache the result of include files, and bitbake classes
"""


class NodeCache:
    """
    Cache to allow linking the BitBake includes, classes and
    requirements.

    The secret of the class will be how we cache
    """
    def __init__(parse_method):
        self.parse_method = parse_method
        self.includes     = {}
        self.classes      = {}


    def parse_class(self, classname, classfile):
        """
        Parse a class or use a cached one
        """
        try:
            return self.classes[classname]
        except KeyError:
            try:
                ast = self.parse_method(classfile,False)
                if ast:
                    self.classes[classname] = ast
                    return ast
                else:
                    raise Exception(), "Can not inherit"
            except:
                raise Exception(), "Class not found/usable", classname

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
                raise Exception(), "Include not found/usable", includename

