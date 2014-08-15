#!/usr/bin/python
# Author: JuanJo Ciarlante <juanjosec@gmail.com>
# License: GPLv3
#
# vim: sw=4 ts=4 et si
# pylint: disable=C0103,W0223,R0904,R0201,W1401
#
#
"""
Sort urlpaths from an httpd logfile with <ip, urlpath> lines,
by entropy of clients' IPs aggregated altogether (bitwise)"
Q&D shell 1liner to split an apache.log:
  sed -rn 's/(\S+).*GET (\S+).*/\1 \2/p' apache.log |split -l 1000 - outlog-
"""
from mrjob.job import MRJob
import math
import socket


def entropy(string):
    "Calculates the Shannon entropy of a string"
    # get probability of chars in string
    prob = [float(string.count(c)) / len(string)
            for c in dict.fromkeys(list(string))]
    # calculate the entropy
    entropy_val = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy_val


class MREntropyPerURL(MRJob):
    """From (ip, url) input lines, output (entropy_val, (urls...)),
       where entropy is the Shannon entropy value of the concatenation
       of all 32bits ips by url"""

    def input_mapper(self, _, line):
        "split line as urlpath, ip"
        ip, path = line.split()
        yield path, ip

    def urlpath_to_entropy(self, key, values):
        "calculate the entropy of all bits from the aggregation of 32bits IPs"
        ip_bits = ""
        for ip in values:
            try:
                ip_bits += socket.inet_aton(ip)
            except socket.error:
                continue
        yield key, str(entropy(ip_bits))

    def swap_values(self, key, value):
        "swap key,value to get output aggregated by entropy_val"
        yield value, key

    def values_per_key(self, key, values):
        "just aggregate the values as a string"
        yield key, " ".join(list(values))

    def steps(self):
        "concatenate both MRs"
        return [self.mr(mapper=self.input_mapper,
                        reducer=self.urlpath_to_entropy),
                self.mr(mapper=self.swap_values,
                        reducer=self.values_per_key)]

if __name__ == '__main__':
    MREntropyPerURL.run()
