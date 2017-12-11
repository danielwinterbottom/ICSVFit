
import sys
import os
from optparse import OptionParser
import math
import fnmatch

parser = OptionParser()

parser.add_option("--folder", dest = "folder",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--dcache_dir", dest = "dcache_dir",
                  help="Specify folder that contains the output to be hadded")

(options,args) = parser.parse_args()

if not options.folder:
  parser.error('No folder specified')


subdirs = ['','TSCALE_DOWN','TSCALE_UP','TSCALE0PI_UP','TSCALE0PI_DOWN','TSCALE1PI_UP','TSCALE1PI_DOWN','TSCALE3PRONG_UP','TSCALE3PRONG_DOWN','EFAKE0PI_UP','EFAKE0PI_DOWN', 'EFAKE1PI_UP', 'EFAKE1PI_DOWN','MUFAKE0PI_UP','MUFAKE0PI_DOWN','MUFAKE1PI_UP','MUFAKE1PI_DOWN','METUNCL_UP','METUNCL_DOWN','METCL_UP','METCL_DOWN']


for subdir in subdirs:
  folder = '%s/%s/' %(options.folder,subdir)  
  dcache_dir = '%s/%s/' % (options.dcache_dir,subdir)
  print "Copying sv fit input files from:", folder
  copy_command='./scripts/copy_to_dcache.sh %s %s 1 %s' % (folder,dcache_dir,subdir)
  #copy_command='./scripts/copy_to_dcache.sh %s %s' % (folder,dcache_dir) # this doesn't use batch

  os.system(copy_command)
