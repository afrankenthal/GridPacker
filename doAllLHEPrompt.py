#! /usr/bin/env python

import os, sys
import subprocess

if (len(sys.argv) != 2):
	print 'Only 1 argument should be provided, the gridpack path (assume prompt decays of chi2)'
	exit(1)

#gridpackdir = os.listdir(os.getcwd()+"/producedgridpacks/ctau1000/")
gp = sys.argv[1]

#for gp in gpdir:
if('iDM_Mchi' in gp) and ('ctau' in gp):


	#### Command 0: Move gridpack to right location IF not already there
	if ("_slc6_amd64_" in gp):
		newname = os.path.basename(gp).split("_slc6_amd64_")[0] + ".tar.xz"
		cmd = 'mv %s GridPacks/%s' % (gp, newname)
		os.system(cmd)
	else:
		newname = os.path.basename(gp)

	import random
	rnum = random.randint(1e5, 1e6)
	#### Command 2: Extract LHE from gridpack
	cmd1 = './extractLHEFromGridpack.py GridPacks/%s %d %s' % (newname, rnum, '0.0')
	process = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
	for line in iter(process.stdout.readline,b''):
		print line,
	process.stdout.close()
	process.wait()

	lhe = newname.split("ctau-")[0] + 'ctau-' + '0p0' + "/" + newname.split(".")[0] + "_" + str(rnum) + ".lhe"
	lhedir = lhe.split('/')[0] 

	#### Command 4: gzip resulting LHE
	cmd3 = "gzip LHEs/%s" % (lhe)
	os.system(cmd3)
	print "done: ", gp

	#### Command 5: transfer gzipped LHE to EOS
	cmd4 = "mkdir -p /eos/user/a/asterenb/iDM/LHE_Samples/%s" % lhedir
	os.system(cmd4)
	cmd5 = "xrdcp LHEs/%s.gz root://eosuser.cern.ch//eos/user/a/asterenb/iDM/LHE_Samples/%s.gz" % (lhe, lhe)
	os.system(cmd5)
	cmd6 = "rm LHEs/%s.gz" % lhe
	os.system(cmd6)
