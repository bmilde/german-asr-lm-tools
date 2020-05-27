#!/bin/bash

for f in split/line*; do
   echo "process $i"
   python3 normalize_subs_sentences.py $f norm/$f &
done

wait

echo "all done!"
