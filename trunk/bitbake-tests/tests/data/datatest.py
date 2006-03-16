"""
Unit Tests for the BitBake Data Module

Copyright 2006 Holger Freyther <freyther@handhelds.org>

USE this code for whatever purpose you want to use it
"""


import unittest

class DataSmartTestCase(unittest.TestCase):
    """
    Test Case for the DataSmart Implementation!
    """
    def testGVar(self):
        # import the data module
        from bb import data
        from bb import data_smart

        d = data_smart.DataSmart()
        data.setVar('TEST', 'testcontents', d )
        self.assertEquals( data.getVar('TEST',d), 'testcontents', 'Setting Variable Failed')
        data.delVar('TEST', d)
        self.assertEquals(data.getVar('TEST', d), None)

    def testVarFlag(self):
        # import the data modules
        from bb import data
        from bb import data_smart

        d = data_smart.DataSmart()
        data.setVarFlag('TEST', 'testflag', 1, d)
        self.assertEquals(data.getVarFlag('TEST', 'testflag', d), 1)
        data.delVarFlag('TEST', 'testflag', d)
        self.assertEquals(data.getVarFlag('TEST', 'testflag', d), None)

        # test that changing a variable is working as well
        data.setVarFlag('TEST', 'testflag', 1, d)
        self.assertEquals(data.getVarFlag('TEST', 'testflag', d), 1)
        data.setVarFlag('TEST', 'testflag', 2, d)
        self.assertEquals(data.getVarFlag('TEST', 'testflag', d), 2)

    def testVarFlags(self):
        # import the data modules
        from bb import data
        from bb import data_smart

        d = data_smart.DataSmart()
        myflags = {}
        myflags['test'] = 'blah'
        myflags['blah'] = 'test'
        data.setVarFlags('TEST', myflags, d)
        self.assertEquals(data.getVarFlags('TEST',d)['blah'], 'test')
        self.assertEquals(data.getVarFlags('TEST',d)['test'], 'blah')

        data.setVarFlags('TEST', { 'abc' : 10}, d)
        self.assertTrue(data.getVarFlags('TEST',d).has_key('abc'))

        # delete the flags now
        data.delVarFlags('TEST', d)
        self.assertEquals(data.getVarFlags('TEST',d), None)

    def testExpansion(self):
        # import the data modules
        from bb import data
        from bb import data_smart

        d = data_smart.DataSmart()
        data.setVar('TEST', 'moo', d)
        self.assertEquals(data.getVar('TEST',d), 'moo')

        # standard expansion
        self.assertEquals(data.expand('/usr/bin/${TEST}', d), '/usr/bin/moo' )

        # python expansion
        self.assertEquals(data.expand('result: ${@37*72}', d), 'result: 2664' )

        # shell expansion
        self.assertEquals(data.expand('${TARGET_FOO}', d), '${TARGET_FOO}')

        data.setVar('TARGET_FOO', 'yeah', d)
        self.assertEquals(data.expand('${TARGET_FOO}', d), 'yeah')

        data.setVar('SRC_URI', 'http://oe.handhelds.org/${TARGET_FOO}', d)
        self.assertEquals(data.expand('${SRC_URI}',d), 'http://oe.handhelds.org/yeah')

        data.delVar('TARGET_FOO', d)
        self.assertEquals(data.expand('${SRC_URI}',d), 'http://oe.handhelds.org/${TARGET_FOO}')


    def testExpandKeys(self):
        pass

    def testExpandData(self):
        pass

    def testEmitVar(self):
        pass

    def testUpdateData(self):
        pass

if __name__ == '__main__':
    unittest.main()
