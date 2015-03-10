#!/bin/bash

set -e

cd ..
# Check if the argument is null
if [ ! -n "$1" ] ;then
    echo "No Wikipedia dump URL entered!"
    echo "Usage:"
    echo "./extract_verbs.sh WikipediaDumpURL"   
fi
# Get the Wikimedia Dump URL
wikimediaDumpURL=$1
# Download latest Wikipedia dump
wget -o wikipedia-dump.xml.bz2 $wikimediaDumpURL
# Extract text
bzcat wikipedia-dump.xml.bz2 | scripts/lib/WikiExtractor.py -o extracted/
# Split extraction by article
mkdir corpus
cat extracted/*/* | csplit --suppress-matched -z -f 'corpus/doc_' - '/</doc>/' {*}
# Build a single big file
find extracted -type f -exec cat {} \; > all-extracted.txt
# Extract verbs with TreeTagger
# N.B. treetagger segfaults with the single big file, run it over each article instead
#cat all-extracted.txt | treetagger/cmd/tree-tagger-chinese | grep VER | sort -u > verbi.txt
find extracted -type f -exec bash -c "cat '{}' | treetagger/cmd/tree-tagger-chinese | grep VER >> verbi.txt" \;
sort -u verbi.txt > unique-sorted-verbs.txt
# Extract vocabulary
python scripts/bag_of_words.py all-extracted.txt
# POS tagging + chunker with TextPro
perl textpro.pl -verbose -html -l ita -c token+sentence+pos+chunk -o . ~/srl/training/zhwiki/gold
