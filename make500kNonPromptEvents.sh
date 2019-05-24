#!/bin/bash

# Argument 1: directory of prompt samples in EOS 
# Argument 2: lifetime argument in mm

if [ $# -ne 2 ];
    then echo "Illegal number of parameters: 2 required (directory in EOS and lifetime in mm)"
fi

ctau=$(echo $2 | sed "s/\./p/g")
echo $ctau

eosbasepath="/eos/user/a/asterenb/iDM/LHE_Samples"
eospathprompt="$eosbasepath/$1"
base=$(basename -- "$1" | sed "s/ctau-0p0/ctau-$ctau/g")
eospathlifetime="$eosbasepath/$base"
echo "Original prompt path: $eospathprompt"
echo "New non-prompt path: $eospathlifetime"

for sample in `ls $eospathprompt`; do
	echo "Processing $sample"
	echo "Copying from EOS to local"
	xrdcp root://eosuser.cern.ch/$eospathprompt/$sample .
	echo "Uncompressing"
	gzip -c -d $sample > temporaryLHE.lhe
	rm $sample
	echo "Replacing lifetime"
	./replaceLHELifetime.py -i temporaryLHE.lhe -t $2 -o temporaryLHE_replaced.lhe
	rm temporaryLHE.lhe
	echo "Recompressing"
	newsample=$(echo $sample | sed "s/ctau-0p0/ctau-$ctau/g")
	gzip -c temporaryLHE_replaced.lhe > $newsample
	rm temporaryLHE_replaced.lhe
	echo "Copying from local to EOS"
	mkdir -p $eospathlifetime
	xrdcp $newsample root://eosuser.cern.ch/$eospathlifetime/
	rm $newsample
done

