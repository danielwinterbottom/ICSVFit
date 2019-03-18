#python scr:ipts/submit_crab_jobs.py --folder=/vols/cms/dw515/Offline/output/SM/Nov24_SVFit/ --dcache_dir=/store/user/dwinterb/SVFit_Nov24


import sys
import os
from optparse import OptionParser
import math
import fnmatch

CRAB='SVFit_2016_newsig'

parser = OptionParser()

parser.add_option("--folder", dest = "folder",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--dcache_dir", dest = "dcache_dir",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--crab", dest = "crab",
                  help="Crab task name.")

(options,args) = parser.parse_args()

if options.crab: CRAB = options.crab

if not options.folder:
  parser.error('No folder specified')

subdirs = ['','TSCALE_DOWN','TSCALE_UP','TSCALE0PI_UP','TSCALE0PI_DOWN','TSCALE1PI_UP','TSCALE1PI_DOWN','TSCALE3PRONG_UP','TSCALE3PRONG_DOWN','JES_UP','JES_DOWN', 'MET_SCALE_UP','MET_SCALE_DOWN','MET_RES_UP','MET_RES_DOWN', 'EFAKE0PI_UP', 'EFAKE0PI_DOWN', 'EFAKE1PI_UP', 'EFAKE1PI_DOWN','MUFAKE0PI_UP','MUFAKE0PI_DOWN','MUFAKE1PI_UP','MUFAKE1PI_DOWN','METUNCL_UP','METUNCL_DOWN','ESCALE_UP','ESCALE_DOWN','JESFULL_DOWN','JESFULL_UP','JESCENT_UP','JESCENT_DOWN','JESHF_UP','JESHF_DOWN','JESRBAL_UP','JESRBAL_DOWN','JESRSAMP_UP','JESRSAMP_DOWN','JES_CORR_UP','JES_CORR_DOWN','JES_UNCORR_UP','JES_UNCORR_DOWN','JESFULL_CORR_DOWN','JESFULL_CORR_UP','JESCENT_CORR_UP','JESCENT_CORR_DOWN','JESHF_CORR_UP','JESHF_CORR_DOWN','JESFULL_UNCORR_DOWN','JESFULL_UNCORR_UP','JESCENT_UNCORR_UP','JESCENT_UNCORR_DOWN','JESHF_UNCORR_UP','JESHF_UNCORR_DOWN','JESBBEE1_DOWN','JESBBEE1_UP','JESBBEE1_UNCORR_DOWN','JESBBEE1_UNCORR_UP','JESBBEE1_CORR_DOWN','JESBBEE1_CORR_UP','JESEE2_DOWN','JESEE2_UP','JESEE2_UNCORR_DOWN','JESEE2_UNCORR_UP','JESEE2_CORR_DOWN','JESEE2_CORR_UP']


for subdir in subdirs:
  folder = '%s/%s/' %(options.folder,subdir)  
  dcache_dir = '%s/%s%s/' % (options.dcache_dir,CRAB,subdir)
  print "Copying outputs from:", dcache_dir
  copy_command='./scripts/copy_from_dcache.sh %s %s 0 ' % (dcache_dir,folder)
  #copy_command='./scripts/copy_from_dcache.sh %s %s 1 %s' % (dcache_dir,folder,subdir) # this will use batch

  os.system(copy_command)
