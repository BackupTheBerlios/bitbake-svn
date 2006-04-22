"""
Unit Tests for the BitBake COW Data

Copyright 2006 Holger Freyther <freyther@handhelds.org>

USE this code for whatever purpose you want to use it
"""


import unittest

class COWTestCase(unittest.TestCase):
    """
    Test case for the COW module from mithro
    """

    def testGetSet(self):
        """
        Test and set
        """
        from bb.COW import COWBase
        a = COWBase

        self.assertEquals(False, a.haskey('a'))

        a['a'] = 'a'
        a['b'] = 'b'
        self.assertEquals(True, a.haskey('a'))
        self.assertEquals(True, a.haskey('b'))
        self.assertEquals('a', a['a'] )
        self.assertEquals('b', a['b'] )

        # check the number of hit keys
        for x in a.iterkeys():
            print x


    def testCopyCopy(self):
        """
        Test the copy of copies
        """

        from bb.COW import COWBase


        # create two COW dict 'instances'
        b = COWBase
        c = COWBase

        # assign some keys to one instance, some keys to another
        b['a'] = 10
        b['c'] = 20
        c['a'] = 30

        # test separation of the two instances
        self.assertEquals(False, c.haskey('c'))
        self.assertEquals(30, c['a'])
        self.assertEquals(10, a['a'])

        # test copy
        b_2 = b.copy()
        c_2 = c.copy()

        self.assertEquals(False, c_2.haskey('c'))
        self.assertEquals(10, b_2['a'])

        b_2['d'] = 40
        self.assertEquals(False, c_2.haskey('d'))
        self.assertEquals(True, b_2.haskey('d'))
        self.assertEquals(40, b_2.haskey('d'))
        self.assertEquals(False, b.haskey('d'))
        self.assertEquals(False, c.haskey('d'))

        c_2['d'] = 30
        self.assertEquals(True, c_2.haskey('d'))
        self.assertEquals(True, b_2.haskey('d'))
        self.assertEquals(30, c_2['d'])
        self.assertEquals(40, b_2['d'])
        self.assertEquals(False, b.haskey('d'))
        self.assertEquals(False, c.haskey('d'))

        # test copy of the copy
        c_3 = c_2.copy()
        b_3 = b_2.copy()
        b_3_2 = b_2.copy()

        c_3['e'] = 4711
        self.assertEquals(4711, c_3['e'])
        self.assertEquals(False, c_2.haskey('e'))
        self.assertEquals(False, b_3.haskey('e'))
        self.assertEquals(False, b_3_2.haskey('e'))
        self.assertEquals(False, b_2.haskey('e'))

        b_3['e'] = 'viel'
        self.assertEquals('viel', b_3['e'])
        self.assertEquals(4711, c_3['e'])
        self.assertEquals(False, c_2.haskey('e'))
        self.assertEquals(False, b_3.haskey('e'))
        self.assertEquals(False, b_3_2.haskey('e'))
        self.assertEquals(False, b_2.haskey('e'))

    def testCow(self):
        from bb.COW import COWBase
        c = COWBase
        c['123'] = 1027
        c['other'] = 4711
        c['d'] = { 'abc' : 10, 'bcd' : 20 }

        copy = c.copy()

        self.assertEquals(1027, c['123'])
        self.assertEquals(4711, c['other'])
        self.assertEquals({'abc':10, 'bcd':20}, c['d'])
        self.assertEquals(1027, copy['123'])
        self.assertEquals(4711, copy['other'])
        self.assertEquals({'abc':10, 'bcd':20}, copy['d'])

        # cow it now
        copy['123'] = 1028
        copy['other'] = 4712
        copy['d']['abc'] = 20

        self.assertEquals(1027, c['123'])
        self.assertEquals(4711, c['other'])
        self.assertEquals({'abc':10, 'bcd':20}, c['d'])
        self.assertEquals(1028, copy['123'])
        self.assertEquals(4712, copy['other'])
        self.assertEquals({'abc':20, 'bcd':20}, copy['d'])

if __name__ == '__main__':
    unittest.main()
