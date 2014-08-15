#!/usr/bin/python
from mrjob.job import MRJob
from mrjob.compat import get_jobconf_value

class FileProtocol(object):
    def write(self, key, value):
        open('/tmp/idx/' + key, "w").write(value)

class MRGrep(MRJob):
    OUTPUT_PROTOCOL = FileProtocol
    def mapper(self, _, line):
        for word in line.split():
            yield word, get_jobconf_value('map.input.file')

    def reducer(self, key, values):
        yield key, str(sorted(set(values)))

if __name__ == '__main__':
    MRGrep.run()
