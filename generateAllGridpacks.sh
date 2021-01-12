#!/bin/bash

dmchis=(0.01 0.1 0.2 0.4)
#m1s=(1 3)
m1s=(1 3 5 10 20 30 40 60 80 100)

for m1 in "${m1s[@]}"; do
	for dmchi in "${dmchis[@]}"; do
		m2=$(echo $m1+$dmchi*$m1 | bc)
		echo "Sending " $m1 " and " $m2 " to submit.py..."
		./submit.py $m1 $m2
	done
	until `bjobs 2>&1 | grep -q unfinished`; do
		sleep 10
		echo "Wating for current LSF jobs to finish..."
	done
	echo "Finished previous iteration, starting new one now..."
done
