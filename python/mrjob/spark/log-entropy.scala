// vim: et si ts=4 sw=4
import scala.collection.mutable.HashMap
def entropy(str: String): Double = {
	var charCount = new HashMap[Char, Int]
	for (c <- str) charCount.put(c, charCount.getOrElse(c, 0) + 1)
	val prob = charCount.map(r => r._2.toDouble / str.length)
	return -prob.map(r => r * math.log(r) / math.log(2.0)).reduce(_ + _)
}
def inet_aton(ip: String): Long = {
    ip.split('.').
        zipWithIndex.foldLeft(0L)(
            (a,b)=>(a + (b._1.toLong << ((3 - b._2)*8))
        )
    )
}
def entropyMap(countBykey: Map[String, Int]): Double = {
    var totalCount = countBykey.foldLeft(0)((a, b) => a + b._2)
	val prob = countBykey.map(r => r._2.toDouble / totalCount)
	return -prob.map(r => r * math.log(r) / math.log(2.0)).reduce(_ + _)
}
def counter(dict: Seq[String]) : Map[String, Int] = {
    dict.groupBy(l => l).map(t => (t._1, t._2.length))
}
val file = sc.textFile("/u/data/star_wars_kid.mini.log")
val file = sc.textFile("/u/data/star_wars_kid.log")
val entroPaths = file.map(r => r.split(" ")).
    map(x => (x.apply(6), x.apply(0))).
    reduceByKey(_ + "|" + _).
    map(x => (entropyMap(counter(x._2.split('|'))), x._1)).
    reduceByKey(_ + " " + _).cache()

val sorterEntroPaths = entroPath.sortBy(_._1)
