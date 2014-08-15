#!/usr/bin/python
from mrjob.job import MRJob
import math
import socket, struct

def entropy(string):
    "Calculates the Shannon entropy of a string"
    # get probability of chars in string
    prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]
    # calculate the entropy
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])
    return entropy

class MREntropyPerURL(MRJob):
    def input_mapper(self, _, line):
        ip, path = line.split()
        yield path, ip

    def urlpath_to_entropy(self, key, values):
        ip_bits = ""
        for ip in values:
            try:
                ip_bits += socket.inet_aton(ip)
            except socket.error:
                continue
        yield key, str(entropy(ip_bits))

    def swap_values(self, key, value):
        yield value, key

    def values_per_key(self, key, values):
        yield key, " ".join(list(values))


    def steps(self):
        return [self.mr(mapper=self.input_mapper,
                        reducer=self.urlpath_to_entropy),
                self.mr(mapper=self.swap_values,
                        reducer=self.values_per_key)]

if __name__ == '__main__':
    MREntropyPerURL.run()
