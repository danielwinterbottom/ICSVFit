#!/usr/bin/env python

import fnmatch
import os
import ROOT
import sys
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-i","--input_folder", dest="input",
                  help="Scan the speciified folder recursively looking for svfit input files." % vars())
parser.add_option("-d","--dcache_path", dest="dcache_path",
                  help="dcache directory to copy files to" % vars())



(options, args) = parser.parse_args()

dcache_path = 'srm://gfe02.grid.hep.ph.ic.ac.uk:8443/srm/managerv2?SFN=/pnfs/hep.ph.ic.ac.uk/data/cms/'+options.dcache_path
for root, dirnames, filenames in os.walk(options.input):
  for filename in fnmatch.filter(filenames, '*svfit_*_input.root'):
    fullfile = os.path.join(root, filename)
    print 'copying %(fullfile)s'%vars()
    os.system('lcg-cp %(fullfile)s %(dcache_path)s/%(filename)s'%vars())

print "Finished copying files"
