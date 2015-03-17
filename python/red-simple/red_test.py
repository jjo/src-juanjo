#!/usr/bin/python
"RED (random early drop) simple implementation: tests"
from red import request_ok
import unittest
import random
# pylint: disable=C0103,C0111,R0904


class TestRed(unittest.TestCase):
    def setUp(self):
        random.seed(0xdeadbeef)
        self.th_min = 0.8
        self.th_max = 1.6
        self.n_times = 1000

    def test_unloaded(self):
        """Load just below th_min must always return OK"""
        for _ in xrange(self.n_times):
            self.assertTrue(
                request_ok(0.99 * self.th_min, self.th_min, self.th_max))

    def test_overloaded(self):
        """Load just above th_max must never return OK"""
        for _ in xrange(self.n_times):
            self.assertFalse(
                request_ok(1.01 * self.th_max, self.th_min, self.th_max))

    def test_someloads(self):
        """For various loads, do a montecarlo run comparing request_ok ratio
          1000 times against expected_ok_ratio (complement of load_ratio)"""
        for load_ratio in (0.0, 0.25, 0.50, 0.75, 1.0):
            load = load_ratio * (self.th_max - self.th_min) + self.th_min
            n_ok = 0.0
            for _ in xrange(self.n_times):
                n_ok = n_ok + (request_ok(load, self.th_min, self.th_max))
            expected_ok_ratio = 1 - load_ratio
            ok_ratio = n_ok / self.n_times
            # allow 5% difference:
            self.assertTrue((expected_ok_ratio - ok_ratio) ** 2 < 0.05 ** 2)

if __name__ == '__main__':
    unittest.main()
