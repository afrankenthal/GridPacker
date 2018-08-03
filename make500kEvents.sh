#!/bin/bash

echo "Generating first LHE batch from GridPack..."

./doAllLHE.py $1

base=$(basename -- "$1" | awk '{split($0, a, "_slc6_amd64_"); print a[1]}')
filename="GridPacks/$base.tar.xz"

for i in `seq 2 4`; do
	echo "Generating batch number $i from GridPack"
	./doAllLHE.py $filename
done
