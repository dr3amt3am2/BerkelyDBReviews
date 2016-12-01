#!/bin/bash
rm -fr scout.txt rtout.txt rwout.txt ptout.txt 
db_dump -p -f rwout.txt rw.idx
db_dump -p -f ptout.txt pt.idx
db_dump -p -f rtout.txt rt.idx
db_dump -p -f scout.txt sc.idx



