#!/bin/bash
rm -f *.txt *.idx
cp ../p1/reviews.txt reviews.txt
sort -fuo pterms.txt ../p1/pterms.txt
sort -fuo rterms.txt ../p1/rterms.txt
sort -fuo scores.txt ../p1/scores.txt
echo Sorting Completed.
python3 format.py 
db_load -T -f rwm.txt -t hash rw.idx
db_load -T -c duplicates=1 -f ptm.txt -t btree pt.idx
db_load -T -c duplicates=1 -f rtm.txt -t btree rt.idx
db_load -T -c duplicates=1 -f scm.txt -t btree sc.idx
rm -r *.txt
echo Index Building Completed.


