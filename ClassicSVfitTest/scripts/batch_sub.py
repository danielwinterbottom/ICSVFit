#!/usr/bin/env python
import fnmatch
import os
import ROOT
import sys
from optparse import OptionParser

JOBWRAPPER 			= './scripts/generate_job.sh'
JOBSUBMIT 			= 'true'
if "JOBWRAPPER" in os.environ: 			JOBWRAPPER 			= os.environ["JOBWRAPPER"] 
if "JOBSUBMIT"  in os.environ: 			JOBSUBMIT 			= os.environ["JOBSUBMIT"]
print "Using job-wrapper:    " + JOBWRAPPER
print "Using job-submission: " + JOBSUBMIT

parser = OptionParser()
parser.add_option("--jobwrap", dest="wrap",
                  help="Specify the job-wrapper script. The current wrapper is '%(JOBWRAPPER)s'."
                  " Using the --wrapper option overrides both the default and the environment variable. " % vars())

parser.add_option("--jobsub", dest="sub",
                  help="Specify the job-submission method. The current method is '%(JOBSUBMIT)s'"
                  " Using the --jobsub option overrides both the default and the environment variable. " % vars())

parser.add_option("-i","--input_folder", dest="input",
                  help="Scan the specified folder recursively looking for svfit input files." % vars())

parser.add_option("--submit", dest="submit", action='store_true', default=False,
                  help="Generate and submit jobs")

parser.add_option("--verify", dest="verify", action='store_true', default=False,
                  help="Run verification of output, if --submit is also set then only jobs failing verification will be resubmitted.")
parser.add_option("--channels", dest="channels", default='em,et,mt,tt',
                  help="Comma seperated list of channels to process, other channels will be ignored." % vars())
parser.add_option("--parajobs", dest="parajobs", action='store_true', default=False,
                  help="Submit jobs parametrically.")
parser.add_option("--jobname", dest="jobname", default='',
                  help="Append extra name to para job .sh file")


(options, args) = parser.parse_args()

channels = options.channels.split(',')

if options.wrap: JOBWRAPPER=options.wrap
if options.sub: 	JOBSUBMIT=options.sub

ROOT.gSystem.Load("libFWCoreFWLite")
ROOT.gSystem.Load("libUserCodeICHiggsTauTau")
ROOT.FWLiteEnabler.enable()

filesSeen = 0
filesVerified = 0

para_out=''
perJob=1
calls=0
parajob_name='parajob%s.sh' % options.jobname
if options.parajobs:
  os.system('%(JOBWRAPPER)s "%(para_out)s" %(parajob_name)s' % vars())
  os.system("sed -i '/export SCRAM_ARCH/ i\source /vols/grid/cms/setup.sh' %s"%parajob_name) 


for root, dirnames, filenames in os.walk(options.input):
  for filename in fnmatch.filter(filenames, '*svfit_*_input.root'):
    if not any('_'+chan+'_' in filename for chan in channels): continue
    fullfile = os.path.join(root, filename)
    outfile = fullfile.replace('input.root','output.root')
    print 'Found input file: '+fullfile
    filesSeen += 1
    submitTask = True
    if options.verify:
      if (os.path.isfile(outfile)):
        print 'Found output file: '+outfile
        fin =  ROOT.TFile(fullfile)
        tin = fin.Get("svfit")
        fout =  ROOT.TFile(outfile)
        tout = fout.Get("svfit")
        if fout and tout:
          if tin.GetEntries() == tout.GetEntries():
            print 'Both input and output trees have ' + str(tin.GetEntries()) + ' entries, passed verification'
            submitTask = False
            filesVerified += 1
          else:
            print 'Failed verification, input and output trees with different numbers of entries!'
          fin.Close()
          fout.Close()
        else:
            print 'Failed verification, unable to open output file'
            fin.Close()
      else:
        print 'Failed verification, output file not found!'

    if submitTask and options.submit:
      if not options.parajobs:
        job = fullfile.replace('_input.root','.sh')
        os.system('%(JOBWRAPPER)s "ClassicSVFitTest %(fullfile)s  %(job)s' % vars())
        os.system('%(JOBSUBMIT)s %(job)s' % vars())
      else:
        if calls % perJob == 0:
          if calls == 0:
            para_out='if [ $SGE_TASK_ID == %i ]; then \n' % int(calls/perJob+1)
          else:
            with open('%s'%parajob_name, 'a') as file: file.write('%s\n'%para_out)
            para_out='fi\nif [ $SGE_TASK_ID == %i ]; then \n' % int(calls/perJob+1)
        para_out+='  ClassicSVFitTest %(fullfile)s  \n' % vars()
        calls+=1

if options.parajobs:
  with open('%s'%parajob_name, 'a') as file: file.write('%s\nfi \n'%para_out)
  os.system('qsub -q hep.q -cwd -l h_rt=0:180:0 -t 1-%u:1 %s' % (int((calls-1)/perJob+1),parajob_name))

print 'TOTAL SVFit FILES:    '+str(filesSeen)
print 'VERIFIED SVFit FILES: '+str(filesVerified)






