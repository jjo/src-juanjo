#!/usr/bin/python
import math
import re
from pyspark import SparkConf, SparkContext
conf = (SparkConf()
                 .setMaster("local")
                 .setAppName("My app")
                 .set("spark.executor.memory", "1g"))
sc = SparkContext(conf = conf)

def entropy(string):
    "Calculates the Shannon entropy of a string"
    # get probability of chars in string
    prob = [float(string.count(c)) / len(string)
            for c in dict.fromkeys(list(string))]
    # calculate the entropy
    entropy_val = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy_val

def logline_extract(logline):
    match = re.match(r'^(\S+).*GET (\S+)', logline)
    if match:
        return match.groups()
    else:
        return ('', '')

files = '/user/ubuntu/ubuconla/star_wars_kid.log'
files = '/u/data/star_wars_kid.mini.log'

lines = sc.textFile(files)
# smaller sample, to verif:
#   lines = sc.parallelize(sc.textFile(files).take(50))


path_ip = lines.map(
    lambda x: logline_extract(x)).map(lambda x: (x[1], x[0]))

path_concat_ips = path_ip.reduceByKey(
    lambda a, b: a + b)
path_entrop = path_concat_ips.map(
    lambda x: (x[0], round(entropy(x[1]), 2)))
entrop_paths = path_entrop.map(
    lambda x: (x[1], x[0])).reduceByKey(lambda x, y: x + " " + y)

entrop_paths.saveAsTextFile('/u/data/ubuconla/mr-out')
