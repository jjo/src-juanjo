#!/usr/bin/env pyspark --jars /usr/lib/hadoop/lib/hadoop-lzo-0.4.15.jar
file = '/ngrams/eng-us-all/1gram'

# Load file into lines RDD, note it needs
# LZO support
lines = sc.sequenceFile(file)

lines.first()[1].split()

# ('word', year, n_times, n_pages, n_books)
# ('foo', '1994', '900', '200', '2')
#  [0]    [1]      [2]    [3]   [4]
data = lines.map(lambda line: line[1].split())

yearlyLengthAll = data.map(
    lambda arr: (int(arr[1]), float(len(arr[0])) * float(arr[2]))
)

yearlyLength = yearlyLengthAll.reduceByKey(lambda a, b: a + b)

yearlyCount = data.map(
    lambda arr: (int(arr[1]), float(arr[2]))
).reduceByKey(
    lambda a, b: a + b
)

yearlyAvg = yearlyLength.join(yearlyCount).map(
    lambda tup: (tup[0], tup[1][0] / tup[1][1])
)

yearlyAvg.saveAsTextFile('/user/jjo/ngrams-out')
