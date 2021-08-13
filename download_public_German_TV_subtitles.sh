#!/bin/bash

mkdir mediathek_subs/
cd mediathek_subs/

for i in {53001..600000}
do
	echo "trying $i"
	echo "wget -nc --max-redirect 0 https://classic.ardmediathek.de/subtitle/$i"
	wget -nc --max-redirect 0 https://classic.ardmediathek.de/subtitle/$i
done
