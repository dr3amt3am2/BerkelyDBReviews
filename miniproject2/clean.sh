#!/bin/bash
rm -f p1/*.txt
rm -rf p1/__pycache__
cp input.txt p1/ 
echo Clean p1.
rm -f p2/*.txt
rm -f p2/*.idx
echo Clean p2.
rm -f p3/*.idx
rm -rf p3/__pycache__
echo Clean p3.
