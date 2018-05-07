#python scripts/submit_crab_jobs.py --folder=/vols/cms/dw515/Offline/output/SM/Nov24_SVFit/ --dcache_dir=/store/user/dwinterb/SVFit_Nov24


import sys
import os
import subprocess
from optparse import OptionParser
import math
import fnmatch

CRAB = 'Apr24_SVFit_output'

parser = OptionParser()

parser.add_option("--folder", dest = "folder",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--dcache_dir", dest = "dcache_dir",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--copy", dest="copy", action='store_true', default=False,
                  help="Copy inputs to dcache")
parser.add_option("--M", dest = "M", default="",
                  help="If specified hard constrain the di-tau mass by set value.")

(options,args) = parser.parse_args()

mass_constraint=''
if options.M != '': mass_constraint = '--M=%s' % options.M

if not options.folder:
  parser.error('No folder specified')


subdirs = ['','TSCALE_DOWN','TSCALE_UP','TSCALE0PI_UP','TSCALE0PI_DOWN','TSCALE1PI_UP','TSCALE1PI_DOWN','TSCALE3PRONG_UP','TSCALE3PRONG_DOWN','JES_UP','JES_DOWN', 'BTAG_UP','BTAG_DOWN','BFAKE_UP','BFAKE_DOWN','MET_SCALE_UP','MET_SCALE_DOWN','MET_RES_UP','MET_RES_DOWN', 'EFAKE0PI_UP', 'EFAKE0PI_DOWN', 'EFAKE1PI_UP', 'EFAKE1PI_DOWN','MUFAKE0PI_UP','MUFAKE0PI_DOWN','MUFAKE1PI_UP','MUFAKE1PI_DOWN','METUNCL_UP','METUNCL_DOWN','METCL_UP','METCL_DOWN','MUSCALE_UP','MUSCALE_DOWN','ESCALE_UP','ESCALE_DOWN','JESFULL_DOWN','JESFULL_UP','JESCENT_UP','JESCENT_DOWN','JESHF_UP','JESHF_DOWN','JESRBAL_UP','JESRBAL_DOWN','MET_SCALE_NJETS0_DOWN','MET_SCALE_NJETS0_UP','MET_SCALE_NJETS1_DOWN','MET_SCALE_NJETS1_UP','MET_SCALE_NJETS2_DOWN','MET_SCALE_NJETS2_UP','MET_RES_NJETS0_DOWN','MET_RES_NJETS0_UP','MET_RES_NJETS1_DOWN','MET_RES_NJETS1_UP','MET_RES_NJETS2_DOWN','MET_RES_NJETS2_UP']


for subdir in subdirs:
  folder = '%s/%s/' %(options.folder,subdir)  
  dcache_dir = '/%s/%s/' % (options.dcache_dir,subdir)
  print 'Processing directory', folder 
  if options.copy:
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
    os.system('python scripts/copy_svfit_input_files_to_dcache.py -i %s -d %s --checkExists' % (folder,dcache_dir)) 
  
  # check if all the inputs are on the dcache before submitting
  try: check_dcache = subprocess.check_output("xrd gfe02.grid.hep.ph.ic.ac.uk:1097 ls %s | grep input | grep .root" % dcache_dir, shell=True).split('\n')
  except: check_dcache = []
  try: check_dir = subprocess.check_output("ls %s/ | grep input.root" % folder, shell=True).split('\n')
  except: check_dir = []
  check_dir = [x for x in check_dir if '.root' in x and 'input' in x]
  check_dcache = [x for x in check_dcache if '.root' in x and 'input' in x]

  print  len(check_dcache), len(check_dir) 
  if len(check_dcache) != len(check_dir): 
    print subdir
    print "dcache and directory do not have the same number of input files, not submtting jobs"
    continue

  print 'Submitting jobs..'
  dcache_dir = 'root://gfe02.grid.hep.ph.ic.ac.uk:1097/%s/%s/' % (options.dcache_dir,subdir)
  name = '%s%s' % (CRAB,subdir)
  submit_command = './scripts/crabsub.py -i %s --name %s --area %s --file_prefix %s %s' % (folder,name,CRAB,dcache_dir, mass_constraint)
  os.system(submit_command)
