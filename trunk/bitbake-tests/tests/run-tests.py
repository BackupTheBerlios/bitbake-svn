#
# (C)opyright 2006 Holger Hans Peter Freyther
#

import unittest

def suite():
    from bblib import bblibtest
    from cow   import cowtest
    from data  import datatest
    from parse import parsetest
    from modules import moduletest
    from bugs  import regtests

    suite1 = unittest.makeSuite(bblibtest.BBModuleTestCase)
    suite2 = unittest.makeSuite(cowtest.COWTestCase)
    suite3 = unittest.makeSuite(datatest.DataSmartTestCase)
    suite4 = unittest.makeSuite(parsetest.BBParserTestPython)
    suite5 = unittest.makeSuite(parsetest.BBParserTestC)
    suite6 = unittest.makeSuite(moduletest.ModuleLoadingTestCase)
    suite7 = unittest.makeSuite(regtests.RegressionTests)

    return unittest.TestSuite((suite1,suite2,suite3,suite4,suite5,suite6,suite7))


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
