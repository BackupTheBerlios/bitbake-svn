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

    suites = []
    suites.append(unittest.makeSuite(bblibtest.BBModuleTestCase))
    suites.append(unittest.makeSuite(datatest.DataSmartTestCase))
    suites.append(unittest.makeSuite(parsetest.BBParserTestPython))
    suites.append(unittest.makeSuite(moduletest.ModuleLoadingTestCase))
    suites.append(unittest.makeSuite(regtests.RegressionTests))

    try:
        from bb import COW
        suites.append(unittest.makeSuite(cowtest.COWTestCase))
    except:
        print "COW is not available"

    try:
        import bb.parser.parse_c
        suites.append(unittest.makeSuite(parsetest.BBParserTestC))
    except:
        print "BitBake C Parser is not available"


    return unittest.TestSuite(suites)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
