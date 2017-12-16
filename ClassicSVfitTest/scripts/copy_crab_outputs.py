#python scripts/submit_crab_jobs.py --folder=/vols/cms/dw515/Offline/output/SM/Nov24_SVFit/ --dcache_dir=/store/user/dwinterb/SVFit_Nov24


import sys
import os
from optparse import OptionParser
import math
import fnmatch

CRAB='Dec11_SVFit'

parser = OptionParser()

parser.add_option("--folder", dest = "folder",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--dcache_dir", dest = "dcache_dir",
                  help="Specify folder that contains the output to be hadded")

(options,args) = parser.parse_args()

if not options.folder:
  parser.error('No folder specified')


subdirs = ['','TSCALE_DOWN','TSCALE_UP','TSCALE0PI_UP','TSCALE0PI_DOWN','TSCALE1PI_UP','TSCALE1PI_DOWN','TSCALE3PRONG_UP','TSCALE3PRONG_DOWN','EFAKE0PI_UP','EFAKE0PI_DOWN', 'EFAKE1PI_UP', 'EFAKE1PI_DOWN','MUFAKE0PI_UP','MUFAKE0PI_DOWN','MUFAKE1PI_UP','MUFAKE1PI_DOWN','METUNCL_UP','METUNCL_DOWN','METCL_UP','METCL_DOWN']

subdirs = ['','TSCALE0PI_UP','TSCALE0PI_DOWN','TSCALE1PI_UP','TSCALE1PI_DOWN','TSCALE3PRONG_UP','TSCALE3PRONG_DOWN','EFAKE0PI_UP','EFAKE0PI_DOWN', 'EFAKE1PI_UP', 'EFAKE1PI_DOWN','MUFAKE0PI_UP','MUFAKE0PI_DOWN','MUFAKE1PI_UP','MUFAKE1PI_DOWN','METUNCL_UP','METUNCL_DOWN','METCL_UP','METCL_DOWN']

for subdir in subdirs:
  folder = '%s/%s/' %(options.folder,subdir)  
  dcache_dir = '%s/%s%s/' % (options.dcache_dir,CRAB,subdir)
  print "Copying outputs from:", dcache_dir
  copy_command='./scripts/copy_from_dcache.sh %s %s 1 %s' % (dcache_dir,folder,subdir)
  #copy_command='./scripts/copy_from_dcache.sh %s %s' % (dcache_dir,folder) # this doesn't use batch

  os.system(copy_command)
