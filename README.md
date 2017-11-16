# ICSVFit

## Setting Up Workarea
setup CMSSW area
```
cmsrel CMSSW_7_6_3
cd CMSSW_7_6_3/src/
cmsenv
git cms-addpkg FWCore/Version
```
clone SV Fit packages
```
git clone https://github.com/SVfit/ClassicSVfit TauAnalysis/ClassicSVfit
git clone https://github.com/SVfit/SVfitTF TauAnalysis/SVfitTF
```
clone IC analysis framework
```
git clone git@github.com:ajgilbert/ICHiggsTauTau.git UserCode/ICHiggsTauTau
```

clone ICSVFit package
```
git clone git@github.com:danielwinterbottom/ICSVFit.git ICSVFit/
```


build 
```
scram b -j8
```

## Submitting the jobs

Move the SVFit input file directory over to ICSVFit/ClassicSVfitTest/<local-folder>, then copy the input files over to dcache (e.g. ICSVFit/ClassicSVfitTest/scripts/copy_svfit_input_files_to_dcache.py or something better). Note that for this code to work the input files on dcache need to all be in the same directory. The files in ICSVFit/ClassicSVfitTest/<local-folder> need to be the same as those in path/to/input/folder/on/dcache

To submit the jobs (after sourcing the crab environment):
```
cd ICSVFit/ClassicSVfitTest
./scripts/crabsub.py -i <local-folder> --name <request name> --area <crab area name> --file_prefix /path/to/input/folder/on/dcache
```

Can then check on the status of jobs with the standard crab commands, once the jobs are done copy the output files back over to the analysis area and untar (crab getoutput should work, then recursive untar) 

In addition to submitting crab jobs, we can also submit them to the batch, for example if we only need to run a very small number of jobs. For example:
```
cd ICSVFit/ClassicSVfitTest
./scripts/batch_sub.py -i <local-folder> --submit --jobsub='./scripts/submit_ic_batch_job.sh "hep.q -l h_rt=0:180:0"'
```
Generates jobs for the input files in <local-folder> and submits them to the IC short queue. The output files are written into <local-folder>
