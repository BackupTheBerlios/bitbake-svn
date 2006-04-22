"""
Unit Test for the BitBake Module.

Copyright 2006 Holger Freyther <freyther@handhelds.org>
USE this code for whatever purpose you want to use it
"""



import unittest
import os.path

(path, name) = os.path.split(__file__)
path = os.path.join(path, 'input')

class BBParserTestCaseBase(unittest.TestCase):
    """
    Base Class for the Parser Tests. The only
    difference between python and c implementation
    is the setup... The tests and files are the
    same. Even the results should be the same.
    """

    def testConfig(self):
        """
        Test .conf file loading and handling
        """
        pass

    def testInclude(self):
        """
        Test including files
        """
        pass

    def testRequire(self):
        """
        Test requiring to be included files
        """
        pass

    def testFlags(self):
        """
        Test if the parser sets the right flags
        """

        pass

    def testTask(self):
        """
        Test task handling of the parser
        """
        pass

    def testHandler(self):
        """
        Test the handling of HANDLERS
        """
        pass

class BBParserTestPython(BBParserTestCaseBase):
    """
    Test Case for BB Library Module
    """

    def setUp(self):
        """
        Make sure we use the python parser
        for the tests
        """
        # Now make sure we use the right parser
        import bb.parse
        from bb.parse.parse_py import ConfHandler
        from bb.parse.parse_py import BBHandler

        bb.parse.handlers = []
        # now set the available handlers
        bh = { 'supports' : BBHandler.supports, 'handle': BBHandler.handle, 'init': BBHandler.init }
        ch = { 'supports' : ConfHandler.supports, 'handle': ConfHandler.handle, 'init': ConfHandler.init }
        bb.parse.handlers.append( ch )
        bb.parse.handlers.append( bh )

class BBParserTestC(BBParserTestCaseBase):
    """
    Test the parser implemented in C
    """

    def setUp(self):
        """
        Use the C parser now
        """
        # Now make sure we use the right parser
        import bb.parse
        from bb.parse.parse_c import BBHandler

        bb.parse.handlers = []
        # now set the available handlers
        bh = { 'supports' : BBHandler.supports, 'handle': BBHandler.handle, 'init': BBHandler.init }
        bb.parse.handlers.append( bh )


if __name__ == '__main__':
    unittest.main()
