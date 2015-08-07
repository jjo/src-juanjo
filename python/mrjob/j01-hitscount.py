#!/usr/bin/python
from mrjob.job import MRJob
import re

class MRHitCount(MRJob):
    def mapper(self, _, line):
        match = re.match(r'^(\S+).*GET ([^\s?]+)', line)
        if match:
            ip, path = match.groups()
            yield path, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRHitCount.run()
