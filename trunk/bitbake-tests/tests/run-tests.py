#
# (C)opyright 2006 Holger Hans Peter Freyther
#

import unittest

def suite():
    from bblib import bblibtest
    from cow   import cowtest
    from data  import datatest
    from parse import parsetest

    suite1 = unittest.makeSuite(bblibtest.BBModuleTestCase)
    suite2 = unittest.makeSuite(cowtest.COWTestCase)
    suite3 = unittest.makeSuite(datatest.DataSmartTestCase)
    suite4 = unittest.makeSuite(parsetest.BBParserTestCase)

    return unittest.TestSuite((suite1,suite2,suite3,suite4))


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
