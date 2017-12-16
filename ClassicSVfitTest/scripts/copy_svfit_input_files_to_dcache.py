#!/usr/bin/env python

import fnmatch
import os
import ROOT
import sys
from optparse import OptionParser
import subprocess

parser = OptionParser()
parser.add_option("-i","--input_folder", dest="input",
                  help="Scan the speciified folder recursively looking for svfit input files." % vars())
parser.add_option("-d","--dcache_path", dest="dcache_path",
                  help="dcache directory to copy files to" % vars())
parser.add_option("--checkExists", dest="checkExists", action='store_true', default=False,
                  help="If set checks if file exists before copying it. If file exists already then it is not copied")

(options, args) = parser.parse_args()

dcache_path = 'srm://gfe02.grid.hep.ph.ic.ac.uk:8443/srm/managerv2?SFN=/pnfs/hep.ph.ic.ac.uk/data/cms/'+options.dcache_path
try: check = subprocess.check_output("xrd gfe02.grid.hep.ph.ic.ac.uk:1097 ls %s | grep input.root" % options.dcache_path, shell=True).split('\n')
except: check = []

for root, dirnames, filenames in os.walk(options.input):
  for filename in fnmatch.filter(filenames, '*svfit_*_input.root'):
    fullfile = os.path.join(root, filename)
    if any(filename in i for i in check) and options.checkExists:
      print 'skipping %(dcache_path)s/%(filename)s because it already exists!' %vars() 
      continue
    print 'copying %(fullfile)s'%vars()
    os.system('lcg-cp %(fullfile)s %(dcache_path)s/%(filename)s'%vars())
  break
print "Finished copying files"
