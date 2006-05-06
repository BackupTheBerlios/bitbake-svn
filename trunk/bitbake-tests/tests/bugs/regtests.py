"""
Regression Testing of BitBake

Copyright 2006 Holger Freyther <freyther@handhelds.org>
USE this code for whatever purpose you want to use it
"""


import unittest, os

(base_path, name) = os.path.split(__file__)
base_path = os.path.abspath(base_path)
path_937 = os.path.join(base_path, 'bug_937')
path_68  = os.path.join(base_path, 'bug_68')

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
        os.environ['BBPATH'] = os.path.join(path_937)
        bitbake = imp.load_source( "bitbake", os.environ['BITBAKE'] )

        os.chdir(path_937)
        cooker = bitbake.BBCooker()
        try:
            cooker.cook( bitbake.BBConfiguration( Opt() ), ["fix-mind"] )
        except SystemExit:
            print "exited"

        self.assertEquals("soft", os.environ['BB_TARGET_FPU'])
        self.assertEquals("true", os.environ['BB_BASE_BBCLAS_RAN'])


    def testBug68(self):
        """
        Selecting the best provider among BitBake collections
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
                    'show_versions' : True,
                    'show_environment' : False,
                    'buildfile' : None
                }

        # set BBPATH
        os.environ['BBPATH'] = os.path.join(path_68)
        bitbake = imp.load_source( "bitbake", os.environ['BITBAKE'] )

        os.chdir(path_68)
        cooker = bitbake.BBCooker()
        try:
            cooker.cook( bitbake.BBConfiguration( Opt() ), [] )
        except SystemExit:
            print "exited"

        (last_ver,last_file,pref_ver,pref_file) = cooker.findBestProvider('test')


        self.assertEquals( ('100', 'r0'), last_ver)
        self.assertEquals('collection2/test_100.bb', last_file)
        self.assertEquals(('100', 'r0'), pref_ver)
        self.assertEquals('collection2/test_100.bb', pref_file)



if __name__ == '__main__':
    unittest.main()
