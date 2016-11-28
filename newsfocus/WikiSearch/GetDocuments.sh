#!/bin/bash

USERNAME=hadoop03
HOST=beret.cs.brandeis.edu

ssh $USERNAME@$HOST << EOF
echo $@
source .bash_profile
cd hadoop-dist
bin/hdfs dfs -rm -r -f result
eval "bin/hadoop jar ~/Wiki.jar edu.brandeis.cs.goldenbear.wikisearch.GetDocumentContent corpusMapFile/part-r-00000 result $@"
rm -r -f ~/result
bin/hdfs dfs -get result ~
EOF

rm DocumentContent
scp -r $USERNAME@$HOST:~/result ./DocumentContent