export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/
export HADOOP_HOME=/usr/lib/hadoop
export HADOOP_CONF_DIR=$PWD/etc
export HADOOP_STREAMING_JAR=$(ls $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar)
alias hadoop-stream="hadoop jar $HADOOP_STREAMING_JAR"
export PATH=$HADOOP_HOME/bin:$PATH
