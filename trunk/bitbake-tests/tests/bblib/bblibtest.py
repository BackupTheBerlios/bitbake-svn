"""
Unit Test for the BitBake Module.

Copyright 2006 Holger Freyther <freyther@handhelds.org>
USE this code for whatever purpose you want to use it
"""


import unittest

_test_dir = 'output'

class BBModuleTestCase(unittest.TestCase):
    """
    Test Case for BB Library Module
    """

    def setUp(self):
        """
        Clean the test directory
        """

        import os
        os.system('rm -r %s > /dev/null 2>&1' % os.path.join(_test_dir,'mkdir'))

    def testMkdir(self):
        """
        Create directories using bb.mkdirhier

        We do that with relative and absolute pathnames
        """
        import bb
        import os
        local_path = os.getcwd()

        # test before we begin. We do not want any files
        self.assertFalse(os.path.exists(os.path.join(_test_dir,'mkdir')))

        # create the directories
        bb.mkdirhier(os.path.join(_test_dir, 'mkdir','foo', 'moo', 'zoo'))
        self.assertEquals(local_path, os.getcwd(), "Still the same directory1")
        self.assertTrue(os.path.exists(os.path.join(_test_dir, 'mkdir','foo','moo','zoo')))
        self.assertFalse(os.path.exists(os.path.join('mkdir')))

        # create now a directory which already exists
        self.assertTrue(os.path.exists(os.path.join(_test_dir, 'mkdir', 'foo')))
        bb.mkdirhier(os.path.join(_test_dir, 'mkdir','foo'))
        self.assertTrue(os.path.exists(os.path.join(_test_dir, 'mkdir', 'foo')))
        self.assertTrue(os.path.exists(os.path.join(_test_dir, 'mkdir', 'foo', 'moo', 'zoo' )))


        # now use absolute paths
        abs = os.path.join(local_path,_test_dir)
        self.assertTrue(os.path.exists(abs))
        bb.mkdirhier(os.path.join(abs,'mkdir','foo','doo'))
        self.assertTrue(os.path.exists(os.path.join(abs,'mkdir','foo','doo')))

        # check that all created directories are present
        self.assertTrue(os.path.exists(os.path.join(_test_dir,'mkdir','foo','doo')))
        self.assertTrue(os.path.exists(os.path.join(_test_dir,'mkdir','foo','moo')))
        self.assertTrue(os.path.exists(os.path.join(_test_dir,'mkdir','foo','moo','zoo')))

        # check that we have no other side effect
        self.assertEquals(local_path, os.getcwd())

    def testMovefile(self):
        pass

    def testDecodeUrl(self):
        pass

    def testEncodeUrl(self):
        pass

    def testWhich(self):
        pass

    def testTokenize(self):
        pass

    def testEvaluate(self):
        pass

    def testFlatten(self):
        pass

    def testRelparse(self):
        pass

    def testVerverify(self):
        pass

    def testIsJustName(self):
        pass

    def testPkgsplit(self):
        pass

    def testCatpkgsplit(self):
        pass

    def testVercmp(self):
        pass

    def testPkgcmp(self):
        pass

    def testDepParenreduce(self):
        pass

    def testDepOpConvert(self):
        pass


if __name__ == '__main__':
    unittest.main()
