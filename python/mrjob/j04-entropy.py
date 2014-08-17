#!/usr/bin/python
# Author: JuanJo Ciarlante <juanjosec@gmail.com>
# License: GPLv3
#
# vim: sw=4 ts=4 et si
# pylint: disable=C0103,W0223,R0904,R0201,W1401
#
#
"""
Sort urlpaths from an apache logfile by entropy of
clients' IPs (bitwise) aggregated altogether, to
get an approximation of clients' diversity
"""
from mrjob.job import MRJob
import math
import socket
import re


def entropy(string):
    "Calculates the Shannon entropy of a string"
    # get probability of chars in string
    prob = [float(string.count(c)) / len(string)
            for c in dict.fromkeys(list(string))]
    # calculate the entropy
    entropy_val = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy_val


def entropy_bits(ips):
    "entropy from concatenated bits for each ipv4"
    return entropy("".join(safe_inet_aton(x) for x in ips))


def safe_inet_aton(ip):
    "inet_aton() with an exception wrapper"
    try:
        return socket.inet_aton(ip)
    except socket.error:
        return ""


class MREntropyPerURL(MRJob):
    """From apache.log input lines, output (entropy_val, (urls...)),
       where entropy is the Shannon entropy value of the concatenation
       of all 32bits ips by url"""

    # 1st MR: urlpath -> entropy([ips])
    def input_mapper(self, _, line):
        "get path, ip from apache logline"
        #ip, path = line.split()
        match = re.match(r'([(\d\.)]+).*GET ([^\s?]+)', line)
        if match:
            ip, path = match.groups()
            yield path, ip

    def urlpath_to_entropy(self, key, values):
        "calculate the entropy of all bits from the aggregation of 32bits IPs"
        yield key, entropy_bits(values)

    # 2nd MR: aggregate all urlpaths by same entropy_val
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
