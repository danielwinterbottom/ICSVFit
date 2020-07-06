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


subdirs = ['', 'TSCALE0PI_UP', 'TSCALE0PI_DOWN', 'TSCALE1PI_UP', 'TSCALE1PI_DOWN', 'TSCALE3PRONG_UP', 'TSCALE3PRONG_DOWN', 'TSCALE3PRONG1PI0_UP', 'TSCALE3PRONG1PI0_DOWN', 'JER_UP', 'JER_DOWN', 'MET_SCALE_UP', 'MET_SCALE_DOWN', 'MET_RES_UP', 'MET_RES_DOWN', 'EFAKE0PI_DOWN', 'EFAKE0PI_UP', 'EFAKE1PI_DOWN', 'EFAKE1PI_UP', 'MUFAKE0PI_DOWN', 'MUFAKE0PI_UP', 'MUFAKE1PI_DOWN', 'MUFAKE1PI_UP', 'MUSCALE_DOWN', 'MUSCALE_UP', 'ESCALE_DOWN', 'ESCALE_UP', 'METUNCL_UP', 'METUNCL_DOWN', 'JESRBAL_DOWN', 'JESRBAL_UP', 'JESABS_DOWN', 'JESABS_UP', 'JESABS_YEAR_DOWN', 'JESABS_YEAR_UP', 'JESFLAV_DOWN', 'JESFLAV_UP', 'JESBBEC1_DOWN', 'JESBBEC1_UP', 'JESBBEC1_YEAR_DOWN', 'JESBBEC1_YEAR_UP', 'JESEC2_DOWN', 'JESEC2_UP', 'JESEC2_YEAR_DOWN', 'JESEC2_YEAR_UP', 'JESHF_DOWN', 'JESHF_UP', 'JESHF_YEAR_DOWN', 'JESHF_YEAR_UP', 'JESRELSAMP_YEAR_DOWN', 'JESRELSAMP_YEAR_UP']


for subdir in subdirs:
  folder = '%s/%s/' %(options.folder,subdir)  
  dcache_dir = '%s/%s%s/' % (options.dcache_dir,CRAB,subdir)
  print "Copying outputs from:", dcache_dir
  copy_command='./scripts/copy_from_dcache.sh %s %s 0 ' % (dcache_dir,folder)
  #copy_command='./scripts/copy_from_dcache.sh %s %s 1 %s' % (dcache_dir,folder,subdir) # this will use batch

  os.system(copy_command)
