#!/usr/bin/env pyspark --jars /usr/lib/hadoop/lib/hadoop-lzo-0.4.15.jar
file = '/ngrams/eng-us-all/1gram'

# Load file into lines RDD, note it needs
# LZO support
lines = sc.sequenceFile(file)

# try 1st w/smaller dataset
# lines = lines.sample(False, 1/1000)

# ('word', year, n_times, n_pages, n_books)
# ('foo', '1994', '900', '200', '2')
#  [0]    [1]      [2]    [3]   [4]
data = lines.map(lambda line: line[1].split())

# Sum counts as -> (year, word): count
# ((1994, 'foo'), 999)
# ((1994, 'bar'), 100)
# :
count_by_year_word = data.map(
    lambda x: ((x[0], int(x[1])), x[2])
).reduceByKey(
    lambda a, b: a+b)

# Rearrange as  -> year: (word, count)
# (1994, ('foo', 999))
# (1994, ('bar', 100))
# :
word_count_by_year = count_by_year_word.map(
    lambda x: (x[0][1], (x[0][0], x[1])))

# Keep only the maximum value, by count
# (1994, ('foo', 999))
# :
max = word_count_by_year.reduceByKey(
    lambda wc1, wc2: wc1 if wc1[1] > wc2[1] else wc2).cache()

max.sortBy(lambda x: x[0]).collect()
