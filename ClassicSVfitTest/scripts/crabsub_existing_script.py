#!/usr/bin/env python
import os
import fnmatch
from optparse import OptionParser

DRY_RUN = False

parser = OptionParser()
parser.add_option("--name",dest="task_name",
                    help="Name of crab task")
parser.add_option("--area",dest="crab_area",
                    help="Crab area name")
parser.add_option("--script", dest="script_name", 
                    help="Script you want to submit")
parser.add_option("--njobs", type=int, dest="jobs",
                    help="Number of jobs to submit")


(options, args) = parser.parse_args()
task_name = options.task_name#"gridsvfittest3"
crab_area = options.crab_area#"Nov292"
outscriptname = options.script_name
jobs = options.jobs

from CRABAPI.RawCommand import crabCommand
from httplib import HTTPException
print '>> crab3 requestName will be %s' %task_name
print '>> crab3 script is %s' %outscriptname

from ICSVFit.ClassicSVfitTest.crab import config
config.General.requestName = task_name
config.JobType.scriptExe = outscriptname
#config.JobType.inputFiles.extend(svfit_files)
config.Data.totalUnits = jobs
config.Data.outputDatasetTag= config.General.requestName
if crab_area is not None:
  config.General.workArea = crab_area
if not DRY_RUN:
  try:
    crabCommand('submit', config=config)
  except HTTPException, hte:
    print hte.headers
