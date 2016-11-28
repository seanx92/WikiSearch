#!/bin/bash

USERNAME=hadoop03
HOST=beret.cs.brandeis.edu

ssh $USERNAME@$HOST << EOF
source .bash_profile
cd hadoop-dist
bin/hdfs dfs -rm -r -f result
eval "bin/hadoop jar ~/Wiki.jar edu.brandeis.cs.goldenbear.wikisearch.QuickQuery InvertedIndexMapfile/part-r-00000 result $@"
rm ~/part-r-00000
bin/hdfs dfs -get result/part-r-00000 ~
EOF

rm TermsDocumentList
scp $USERNAME@$HOST:~/part-r-00000 ./TermsDocumentList


