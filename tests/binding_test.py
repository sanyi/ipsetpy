__author__ = 'sanyi'

import unittest
import ipsetpy.wrapper


class TestBasicBindingFunctions(unittest.TestCase):

    def setUp(self):
        print('setup')

    def test_version(self):
        result = ipsetpy.wrapper.ipset_version()
        self.assertRegex(result, "ipset v\d*.\d*.\d*, protocol version: \d*")

    # TODO: complete tests

if __name__ == '__main__':
    unittest.main()