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
The file_prefix needs to have the full path to the file i.e 'root://gfe02.grid.hep.ph.ic.ac.uk:1097' before the '/store/user/...'

Using the option --M=X will add a constrain on mass to the SV fit computation e.g --M=125.0

Can then check on the status of jobs with the standard crab commands, once the jobs are done copy the output files back over to the analysis area and untar (crab getoutput should work, then recursive untar) 

In addition to submitting crab jobs, we can also submit them to the batch, for example if we only need to run a very small number of jobs. For example:
```
cd ICSVFit/ClassicSVfitTest
./scripts/batch_sub.py -i <local-folder> --submit --jobsub='./scripts/submit_ic_batch_job.sh "hep.q -l h_rt=0:180:0"'
```
Generates jobs for the input files in <local-folder> and submits them to the IC short queue. The output files are written into <local-folder>

## Alternative instructions which tend to be quicker
copy svfit inputs to batch using:

./scripts/copy_to_dcache.sh path/to/svfit/inputs path/to/dcache/dir 1 job_name 

or if running also for the systematic shifted inputs do:

dirs=('' 'TSCALE_UP' 'TSCALE_DOWN' 'TSCALE0PI_UP' 'TSCALE0PI_DOWN' 'TSCALE1PI_UP' 'TSCALE1PI_DOWN' 'TSCALE3PRONG_UP' 'TSCALE3PRONG_DOWN' 'EFAKE0PI_UP' 'EFAKE0PI_DOWN' 'EFAKE1PI_UP' 'EFAKE1PI_DOWN' 'MUFAKE0PI_UP' 'MUFAKE0PI_DOWN' 'MUFAKE1PI_UP' 'MUFAKE1PI_DOWN' 'METUNCL_UP' 'METUNCL_DOWN' 'METCL_UP' 'METCL_DOWN')

for i in "${dirs[@]}"; do ./scripts/copy_to_dcache.sh /path/to/svfit/inputs/$i path/to/dcache/dir/$i 1 $i; done

then submit the jobs using:

python scripts/submit_crab_jobs.py --folder=/vols/cms/dw515/Offline/output/SM/Dec29_SVFit/ --dcache_dir=/store/user/dwinterb/Dec29_SVFit/ --copy

the --copy option will check that the svfit input files exist on the dcache directory and then copy them over if they don't so is only needed to make sure all the inputs were copied correctly in the first step

Using the option --M=X will add a constrain on mass to the SV fit computation e.
g --M=125.0

Once the job have finished the .tar files can be copied using the command:

 python scripts/copy_crab_outputs.py --folder=/path/to/target/directory/ --dcache_dir=/path/to/dcache/output/directory/

which assumes the target directroy has the corret subdirectory structure for the systematic shifted folders. This script also check if the .tar files exists before copying it over so exisiting files won't be overwritten.

The following script can be use to check that the number of .tar output fils matched the number of SV fit input files if they are stored in the same folder:

./scripts/check_copied.sh /vols/cms/dw515/Offline/output/SM/Dec29_SVFit/

This script will also unntar the output files. If the numbers don't match you shoud re-run the copying script.
