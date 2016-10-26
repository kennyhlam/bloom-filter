#!/usr/bin/env python

from bloom_filter import BloomFilter
import unittest
import hashlib


def hex_str(i):
    # converts int to hex before converting into string, since
    # code converts back from hex to decimal
    return str(hex(i))


class TestBloomFilter(unittest.TestCase):

    def test_defaults(self):
        b = BloomFilter()
        self.assertTrue(len(b.bitarray) == 10000)
        self.assertTrue(b.hashes == BloomFilter.default_hashes)

    def test_add_check(self):
        b = BloomFilter()
        self.assertFalse(b.check('dummy'))
        b.add('dummy')
        self.assertTrue(b.check('dummy'))

        b = BloomFilter()
        for i in xrange(len(b.bitarray)):
            inp = hex_str(i)
            b.add(inp)
            self.assertTrue(b.check(inp))

    def test_small_bitarray(self):
        b = BloomFilter(k=1)
        self.assertFalse(b.check('dummy'))
        b.add('dummy')
        self.assertTrue(b.check('dummy'))
        # bitarray length of 1, means everything should match
        self.assertTrue(b.check('not-dummy'))

    def test_hash_collisions(self):
        b = BloomFilter(hashes=lambda x: [x])
        b.add(hex_str(1))
        # this collides cause it's also offset by 1
        collision = hex_str(len(b.bitarray)+1)
        self.assertTrue(b.check(collision))

    def test_check_failures(self):
        b = BloomFilter(hashes=lambda x: [x])
        for i in xrange(5):
            inp = hex_str(i)
            b.add(inp)

        inp = hex_str(5)
        self.assertFalse(b.check(inp))
        inp = hex_str(6)
        self.assertFalse(b.check(inp))

    def test_multi_hashes(self):
        def f(x):
            return [hashlib.md5(x).hexdigest(),
                    hashlib.sha256(x).hexdigest()]

        b = BloomFilter(hashes=f)
        for i in xrange(len(b.bitarray)):
            inp = hex_str(i)
            b.add(inp)
            self.assertTrue(b.check(inp))

        for i in ['dummy', 'test', 'nothing', 'empty', '', 'aaaaaaa', 'kdjf']:
            b.add(i)
            self.assertTrue(b.check(i))


if __name__ == '__main__':
    unittest.main()
