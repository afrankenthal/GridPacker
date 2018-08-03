#! /usr/bin/env python

import os, sys
import subprocess

if (len(sys.argv) != 2):
	print 'Only 1 argument should be provided, the full path and name of the gridpack'
	exit(1)

#gridpackdir = os.listdir(os.getcwd()+"/producedgridpacks/ctau1000/")
gp = sys.argv[1]

#for gp in gpdir:
if('iDM_Mchi' in gp) and ('ctau' in gp):
	ctau_str = gp.split('ctau-')[1].split('_slc6_amd64_')[0]
	ctau = float(ctau_str.replace('p','.'))*10

	newname = os.path.basename(gp).split("_slc6_amd64_")[0] + ".tar.xz"

	#### Command 1: Move gridpack to right location
	cmd = 'mv %s GridPacks/%s' % (gp, newname)
	os.system(cmd)

	import random
	rnum = random.randint(1e5, 1e6)
	#### Command 2: Extract LHE from gridpack
	cmd1 = './extractLHEFromGridpack.py GridPacks/%s %d' % (newname, rnum)
	process = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
	for line in iter(process.stdout.readline,b''):
		print line,
	process.stdout.close()
	process.wait()

	#### Command 3: Replace LHE chi2's lifetime
	lhe = newname.split(".")[0] + "/" + newname.split(".")[0] + "_" + str(rnum) + ".lhe"
	cmd2 = "./replaceLHELifetime.py -i ./LHEs/%s -t %s" % (lhe, ctau)
	process1 = subprocess.Popen(cmd2,shell=True,stdout=subprocess.PIPE)
	print "replacing life with: ", ctau
	process1.wait()

	#### Command 4: gzip resulting LHE
	cmd3 = "gzip LHEs/%s" % (lhe)
	os.system(cmd3)
	print "done: ", gp
