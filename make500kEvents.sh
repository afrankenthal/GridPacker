#!/bin/bash

# Argument 1: gridpack path -- assumes it's a fresh gridpack
# Argument 2: lifetime

echo "Generating first LHE batch from GridPack..."

if [ $# -eq 2 ]; then
	./doAllLHE.py $1 $2
else
	./doAllLHE.py $1
fi

base=$(basename -- "$1" | awk '{split($0, a, "_slc6_amd64_"); print a[1]}')
filename="GridPacks/$base.tar.xz"

for i in `seq 2 2`; do
	echo "Generating batch number $i from GridPack"
	if [ $# -eq 2 ]; then
		./doAllLHE.py $filename $2
	else
		./doAllLhe.py $filename
	fi
done
