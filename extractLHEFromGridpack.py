#!/usr/bin/env python
import os, sys

NEVENTS=1e2
NCPU=4

def setup_CMSSW():
    CMSSW_v = 'CMSSW_7_1_30'
    import pwd
    username = pwd.getpwuid( os.getuid() )[0]
    CMSSW_dir = '/tmp/{0}/{1}/'.format( username, CMSSW_v )
    if os.path.isdir( CMSSW_dir ):
        os.chdir( CMSSW_dir + 'src' )
        os.system('rm -rf *')
    else:
        if not os.path.isdir('/tmp/{0}'.format( username )):
            os.mkdir('/tmp/{0}'.format( username ))
        os.chdir('/tmp/{0}'.format( username ))
        os.system('export SCRAM_ARCH=slc6_amd64_gcc481')
        os.system('scram p CMSSW {0}'.format( CMSSW_v ))
        os.chdir(CMSSW_v+'/src/')
    os.system('scram runtime -sh')
    return os.getcwd()



def main():
    
    lifetime = sys.argv[3]
    cwd = os.getcwd()
    gp = os.path.join(cwd, sys.argv[1])
    lhedir = os.path.join(cwd, 'LHEs')
    lhedir = os.path.join(lhedir, os.path.basename(sys.argv[1]).split('.tar.xz')[0])
    lhedir = lhedir.split('ctau-')[0] + 'ctau-' + lifetime.replace('.','p')
    if (not os.path.isdir(lhedir)):
        os.mkdir(lhedir)

    # setup CMSSW in /tmp
    setup_CMSSW()

    # untar gridpack
    os.system('tar xaf {0}'.format( gp ))

    # get LHE
    #import random
    #rnum = random.randint(1e5, 1e6)
    rnum = sys.argv[2]
    os.system('./runcmsgrid.sh {0} {1} {2}'.format(int(NEVENTS), rnum, NCPU))

    # copy back and renaming
    #gpdir = os.path.join(cwd, 'LHEs')
    #if not os.path.isdir(gpdir):
    #    os.mkdir( gpdir )
    #gpname = 'iDM-'+os.path.basename(sys.argv[1]).split('_slc6_amd64_gcc481_')[0]+'.lhe'
    lhename = os.path.basename(sys.argv[1]).split('.tar.xz')[0] + '_' + str(rnum) + '.lhe'
    os.system('cp cmsgrid_final.lhe {0}'.format(os.path.join(lhedir, lhename)))
    os.chdir(cwd)
    print 'Done.'
    #print os.listdir('./LHEs')
    print os.listdir(lhedir)

if __name__ == "__main__":
    main()
