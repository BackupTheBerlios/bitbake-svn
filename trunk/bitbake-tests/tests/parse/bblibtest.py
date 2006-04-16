"""
Unit Test for the BitBake Module.

Copyright 2006 Holger Freyther <freyther@handhelds.org>
USE this code for whatever purpose you want to use it
"""


import unittest

_test_dir = 'output'

class BBParserTestCase(unittest.TestCase):
    """
    Test Case for BB Library Module
    """

    def __init__(self,methodName='runTest'):
        """
        Clean the test directory
        """
        import os
        os.system('rm -r %s > /dev/null 2>&1' % os.path.join(_test_dir,'mkdir'))
        unittest.TestCase.__init__(self,methodName)

    def testMkdir(self):
        """
        Create directories using bb.mkdirhier

        We do that with relative and absolute pathnames
        """
        import bb
	from bb.parser 

        # test before we begin. We do not want any files
        self.assertFalse(os.path.exists(os.path.join(_test_dir,'mkdir')))



if __name__ == '__main__':
    unittest.main()
