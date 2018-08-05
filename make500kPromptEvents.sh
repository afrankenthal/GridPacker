#!/bin/bash

# Argument 1: gridpack path -- assumes it's a fresh gridpack
# No lifetime argument: assume prompt (0p0)

echo "Generating first LHE batch from GridPack..."

./doAllLHEPrompt.py $1

base=$(basename -- "$1" | awk '{split($0, a, "_slc6_amd64_"); print a[1]}')
filename="GridPacks/$base.tar.xz"

for i in `seq 2 47`; do
	echo "Generating batch number $i from GridPack"
	./doAllLHEPrompt.py $filename
done
