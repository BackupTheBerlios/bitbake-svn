"""
Regression Testing of BitBake

Copyright 2006 Holger Freyther <freyther@handhelds.org>
USE this code for whatever purpose you want to use it
"""


import unittest, os

(path, name) = os.path.split(__file__)
path = os.path.join(path, 'bug_937')


class RegressionTests(unittest.TestCase):
    """
    Try to do regression testing
    """

    def testBug937(self):
        """
        BitBake changed the time when update_data gets called. This
        lead to Cooker.configuration.data not expanding any overrides.
        This lead to TARGET_FPU_arm not been overriden.
        """
        import imp, bb

        class Opt:
            def __init__(self):
                self.__dict__ = {
                    'abort' : False,
                    'interactive' : False,
                    'force' : False,
                    'cmd' : 'build',
                    'file' : [],
                    'verbose' : False,
                    'debug' : 0,
                    'dry_run' : False,
                    'parse_only' : False,
                    'disable_psyco' : False,
                    'show_versions' : False,
                    'show_environment' : False,
                    'buildfile' : None
                }

        # set BBPATH
        os.environ['BBPATH'] = os.path.join(path)
        bitbake = imp.load_source( "bitbake", os.environ['BITBAKE'] )

        os.chdir(path)
        cooker = bitbake.BBCooker()
        cooker.cook( bitbake.BBConfiguration( Opt() ), ["fix-mind"] )

        self.assertEquals("soft", os.environ['BB_TARGET_FPU'])
        self.assertTrue(os.environ['BB_BASE_BBCLAS_RAN'])


if __name__ == '__main__':
    unittest.main()
