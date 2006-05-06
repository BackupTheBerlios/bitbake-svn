"""
Unit Test for loading/importing BitBake modules

Copyright 2006 Holger Freyther <freyther@handhelds.org>
USE this code for whatever purpose you want to use it
"""


import unittest

class ModuleLoadingTestCase(unittest.TestCase):
    """
    Test if all modules can be loaded (no python
    compiler)
    """

    def testShell(self):
        from bb import shell

    def testUtils(self):
        from bb import utils

    def testNote(self):
        from bb import note

    def testError(self):
        from bb import error

    def testData(self):
        from bb import data

    def testEvent(self):
        from bb import event

    def testMethodpool(self):
        from bb import methodpool

    def testManifest(self):
        from bb import manifest

    def testCache(self):
        from bb import cache

    def testBuild(self):
        from bb import build

    def testFetch(self):
        from bb import fetch

    def testParse(self):
        from bb import parse
        


if __name__ == '__main__':
    unittest.main()
