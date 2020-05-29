#!/bin/bash

for i in {0..9}; do
   echo "process 0$i"
   python3 normalize_wiki_sentences.py wikiextractor_output/AA/wiki_0$i.bz2 norm/0$i.txt &
done

for i in {10..46}; do
   echo "process $i"
   python3 normalize_wiki_sentences.py wikiextractor_output/AA/wiki_$i.bz2 norm/$i.txt &
done

wait

echo "all done!"
