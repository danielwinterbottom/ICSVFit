#python scripts/submit_crab_jobs.py --folder=/vols/cms/dw515/Offline/output/SM/Nov24_SVFit/ --dcache_dir=/store/user/dwinterb/SVFit_Nov24


import sys
import os
from optparse import OptionParser
import math
import fnmatch

CRAB = 'Nov24_SVFit'

parser = OptionParser()

parser.add_option("--folder", dest = "folder",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--dcache_dir", dest = "dcache_dir",
                  help="Specify folder that contains the output to be hadded")

(options,args) = parser.parse_args()

if not options.folder:
  parser.error('No folder specified')


subdirs = ['','TSCALE_DOWN','TSCALE_UP','TSCALE0PI_UP','TSCALE0PI_DOWN','TSCALE1PI_UP','TSCALE1PI_DOWN','TSCALE3PRONG_UP','TSCALE3PRONG_DOWN','EFAKE0PI_UP','EFAKE0PI_DOWN', 'EFAKE1PI_UP', 'EFAKE1PI_DOWN','MUFAKE0PI_UP','MUFAKE0PI_DOWN','MUFAKE1PI_UP','MUFAKE1PI_DOWN']


for subdir in subdirs:
  folder = '%s/%s' %(options.folder,subdir)  
  print 'Processing directory', folder 
  # first remove the files that we don't want to compute the SV fit for
  print 'Removing files that aren\'t needed..'
  if 'MUFAKE' in subdir or 'EFAKE' in subdir:
    os.system('ls %s/*.root | grep -v -e DY -e EWKZ | xargs rm' % (folder))
  if 'EFAKE' in subdir:
    os.system('ls %s/*.root | grep -v _et_ | xargs rm' % (folder))
  if 'MUFAKE' in subdir:
    os.system('ls %s/*.root | grep -v _mt_ | xargs rm' % (folder))
  if 'TSCALE_' in subdir:
    os.system('ls %s/*.root | grep -v _em_ | xargs rm' % (folder))
  if 'TSCALE' in subdir and 'TSCALE_' not in subdir:
    os.system('ls %s/*.root | grep _em_ | xargs rm' % (folder))
  
  # then copy the files over to the dcache
  print 'Copying files to dcache..'
  dcache_dir = '/%s/%s' % (options.dcache_dir,subdir)
  os.system('python scripts/copy_svfit_input_files_to_dcache.py -i %s -d %s' % (folder,dcache_dir)) 

  # submit the jobs over crab
  print 'Submitting jobs..'
  dcache_dir = 'root://gfe02.grid.hep.ph.ic.ac.uk:1097/%s/%s' % (options.dcache_dir,subdir)

  submit_command = './scripts/crabsub.py -i %s --name %s --area %s --file_prefix %s' % (folder,CRAB,CRAB,dcache_dir)

  #os.system(submit_command)
