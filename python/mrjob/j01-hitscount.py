#!/usr/bin/python
from mrjob.job import MRJob

class MRHitCount(MRJob):
    def mapper(self, _, line):
        ip, path = split(line)
        yield path, 1

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRHitCount.run()
