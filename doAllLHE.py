#! /usr/bin/env python

import os, sys
import subprocess

if (len(sys.argv) < 2):
	print 'Only 2 arguments should be provided, the gridpack path and the lifetime in cm (optional; if not provided, default is to extract from filename)'
	exit(1)

#gridpackdir = os.listdir(os.getcwd()+"/producedgridpacks/ctau1000/")
gp = sys.argv[1]
if (len(sys.argv) > 2):
	ctau = float(sys.argv[2]) * 10 # now in mm

#for gp in gpdir:
if('iDM_Mchi' in gp) and ('ctau' in gp):

	if (len(sys.argv) < 3):
		if ("_slc6_amd64_" in gp):
			ctau_str = gp.split('ctau-')[1].split('_slc6_amd64_')[0]
			ctau = float(ctau_str.replace('p','.'))*10
		else:
			ctau_str = gp.split('ctau-')[1].split('.tar')[0]
			ctau = float(ctau_str.replace('p','.'))*10

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
	cmd1 = './extractLHEFromGridpack.py GridPacks/%s %d %s' % (newname, rnum, sys.argv[2])
	process = subprocess.Popen(cmd1,shell=True, stdout=subprocess.PIPE)
	for line in iter(process.stdout.readline,b''):
		print line,
	process.stdout.close()
	process.wait()

	#### Command 3: Replace LHE chi2's lifetime
	lhe = newname.split("ctau-")[0] + 'ctau-' + sys.argv[2].replace('.','p') + "/" + newname.split(".")[0] + "_" + str(rnum) + ".lhe"
	cmd2 = "./replaceLHELifetime.py -i ./LHEs/%s -t %s" % (lhe, ctau)
	process1 = subprocess.Popen(cmd2,shell=True,stdout=subprocess.PIPE)
	print "replacing life with: ", ctau
	for line in iter(process1.stdout.readline,b''):
		print line,
	process1.stdout.close()
	process1.wait()

	lhe = lhe.split('ctau-')[0] + 'ctau-' + lhe.split('ctau-')[1] + 'ctau-' + sys.argv[2].replace('.','p') + '_' + lhe.split('_')[-1]
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
	cmd6 = "rm LHEs/%s.gz LHEs/%s" % (lhe, lhe)
	os.system(cmd6)
