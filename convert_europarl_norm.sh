#!/bin/bash

for f in europarl_split/e*; do
   echo "process $i"
   python3 normalize_subs_sentences.py $f europarl_norm/$f &
done

wait

echo "all done!"
