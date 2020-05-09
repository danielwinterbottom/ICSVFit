#python scripts/submit_crab_jobs_new.py --folder=/vols/cms/dw515/Offline/output/SM/Nov24_SVFit/ --dcache_dir=/store/user/dwinterb/SVFit_Nov24 --crab=Nov24_SVFit


import sys
import os
import subprocess
from optparse import OptionParser
import math
import fnmatch

CRAB = 'Oct12_2017_SVFit_output'

parser = OptionParser()

parser.add_option("--folder", dest = "folder",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--dcache_dir", dest = "dcache_dir",
                  help="Specify folder that contains the output to be hadded")
parser.add_option("--copy", dest="copy", action='store_true', default=False,
                  help="Copy inputs to dcache")
parser.add_option("--M", dest = "M", default="",
                  help="If specified hard constrain the di-tau mass by set value.")
parser.add_option("--crab", dest = "crab", default='SVFit_output',
                  help="Name of crab task")

(options,args) = parser.parse_args()

CRAB = options.crab


mass_constraint=''
if options.M != '': mass_constraint = '--M=%s' % options.M

if not options.folder:
  parser.error('No folder specified')


subdirs = ['', 'TSCALE0PI_UP', 'TSCALE0PI_DOWN', 'TSCALE1PI_UP', 'TSCALE1PI_DOWN', 'TSCALE3PRONG_UP', 'TSCALE3PRONG_DOWN', 'TSCALE3PRONG1PI0_UP', 'TSCALE3PRONG1PI0_DOWN', 'JER_UP', 'JER_DOWN', 'MET_SCALE_UP', 'MET_SCALE_DOWN', 'MET_RES_UP', 'MET_RES_DOWN', 'EFAKE0PI_DOWN', 'EFAKE0PI_UP', 'EFAKE1PI_DOWN', 'EFAKE1PI_UP', 'MUFAKE0PI_DOWN', 'MUFAKE0PI_UP', 'MUFAKE1PI_DOWN', 'MUFAKE1PI_UP', 'MUSCALE_DOWN', 'MUSCALE_UP', 'ESCALE_DOWN', 'ESCALE_UP', 'METUNCL_UP', 'METUNCL_DOWN', 'JESRBAL_DOWN', 'JESRBAL_UP', 'JESABS_DOWN', 'JESABS_UP', 'JESABS_YEAR_DOWN', 'JESABS_YEAR_UP', 'JESFLAV_DOWN', 'JESFLAV_UP', 'JESBBEC1_DOWN', 'JESBBEC1_UP', 'JESBBEC1_YEAR_DOWN', 'JESBBEC1_YEAR_UP', 'JESEC2_DOWN', 'JESEC2_UP', 'JESEC2_YEAR_DOWN', 'JESEC2_YEAR_UP', 'JESHF_DOWN', 'JESHF_UP', 'JESHF_YEAR_DOWN', 'JESHF_YEAR_UP', 'JESRELSAMP_YEAR_DOWN', 'JESRELSAMP_YEAR_UP']



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
  try: check_dcache = subprocess.check_output("xrdfs gfe02.grid.hep.ph.ic.ac.uk:1097 ls %s | grep input | grep .root" % dcache_dir, shell=True).split('\n')
  except: check_dcache = []
  try: check_dir = subprocess.check_output("ls %s/ | grep input.root" % folder, shell=True).split('\n')
  except: check_dir = []

  check_dir = [x for x in check_dir if '.root' in x and 'input' in x]
  check_dcache = [x for x in check_dcache if '.root' in x and 'input' in x]

  print  len(check_dcache), len(check_dir) 
  #if len(check_dcache) != len(check_dir): 
  if len(check_dcache) < len(check_dir): 
    print subdir
    print "dcache and directory do not have the same number of input files, not submtting jobs"
    continue

  print 'Submitting jobs..'
  dcache_dir = 'root://gfe02.grid.hep.ph.ic.ac.uk:1097/%s/%s/' % (options.dcache_dir,subdir)
  name = '%s%s' % (CRAB,subdir)


  submit_command = './scripts/crabsub_new.py -i %s --name %s --area %s --file_prefix %s %s' % (folder,name,CRAB,dcache_dir, mass_constraint)
  os.system(submit_command)
