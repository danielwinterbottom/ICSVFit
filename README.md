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

## run all jobs on batch

This is not recommended as it will create many jobs on the batch, much better to use the grid!
First define array of systematic subdirectories you wish o process

  'dirs=('' 'TSCALE_UP' 'TSCALE_DOWN' 'TSCALE0PI_UP' 'TSCALE0PI_DOWN' 'TSCALE1PI_UP' 'TSCALE1PI_DOWN' 'TSCALE3PRONG_UP' 'TSCALE3PRONG_DOWN' 'EFAKE0PI_UP' 'EFAKE0PI_DOWN' 'EFAKE1PI_UP' 'EFAKE1PI_DOWN' 'MUFAKE0PI_UP' 'MUFAKE0PI_DOWN' 'MUFAKE1PI_UP' 'MUFAKE1PI_DOWN' 'METUNCL_UP' 'METUNCL_DOWN' 'METCL_UP' 'METCL_DOWN' 'MUSCALE_UP' 'MUSCALE_DOWN' 'ESCALE_UP' 'ESCALE_DOWN')'

Then submit jobs using:

  'for i in "${dirs[@]}"; do ./scripts/batch_sub.py -i /vols/cms/dw515/Offline/output/SM/Mar19_SVFit/$i/ --submit --jobsub='./scripts/submit_ic_batch_job.sh "hep.q -l h_rt=0:180:0"' --parajobs --jobname=$i; done'

## Alternative instructions which tend to be quicker

copy svfit inputs to dcache using batch:
(not recommeneded to use this option as it creats problem on the batch! - instead use the --copy option when running the submission script to also copy the files before submitting the crab jobs)

./scripts/copy_to_dcache.sh path/to/svfit/inputs path/to/dcache/dir 1 job_name 

or if running also for the systematic shifted inputs do:

dirs=("" "TSCALE_DOWN" "TSCALE_UP" "TSCALE0PI_UP" "TSCALE0PI_DOWN" "TSCALE1PI_UP" "TSCALE1PI_DOWN" "TSCALE3PRONG_UP" "TSCALE3PRONG_DOWN" "JES_UP" "JES_DOWN" "BTAG_UP" "BTAG_DOWN" "BFAKE_UP" "BFAKE_DOWN" "MET_SCALE_UP" "MET_SCALE_DOWN" "MET_RES_UP" "MET_RES_DOWN" "EFAKE0PI_UP" "EFAKE0PI_DOWN" "EFAKE1PI_UP" "EFAKE1PI_DOWN" "MUFAKE0PI_UP" "MUFAKE0PI_DOWN" "MUFAKE1PI_UP" "MUFAKE1PI_DOWN" "METUNCL_UP" "METUNCL_DOWN" "METCL_UP" "METCL_DOWN" "MUSCALE_UP" "MUSCALE_DOWN" "ESCALE_UP" "ESCALE_DOWN" "JESFULL_DOWN" "JESFULL_UP" "JESCENT_UP" "JESCENT_DOWN" "JESHF_UP" "JESHF_DOWN" "JESRBAL_UP" "JESRBAL_DOWN" "MET_SCALE_NJETS0_DOWN" "MET_SCALE_NJETS0_UP" "MET_SCALE_NJETS1_DOWN" "MET_SCALE_NJETS1_UP" "MET_SCALE_NJETS2_DOWN" "MET_SCALE_NJETS2_UP" "MET_RES_NJETS0_DOWN" "MET_RES_NJETS0_UP" "MET_RES_NJETS1_DOWN" "MET_RES_NJETS1_UP" "MET_RES_NJETS2_DOWN" "MET_RES_NJETS2_UP")


for i in "${dirs[@]}"; do ./scripts/copy_to_dcache.sh /path/to/svfit/inputs/$i path/to/dcache/dir/$i 1 $i; done

then submit the jobs using:

python -u scripts/submit_crab_jobs.py --folder=/vols/cms/dw515/Offline/output/SM/Aug14_SVFit/ --dcache_dir=/store/user/dwinterb/Aug14_SVFit/ --copy

the --copy option will check that the svfit input files exist on the dcache directory and then copy them over if they don't so is only needed to make sure all the inputs were copied correctly in the first step

Using the option --M=X will add a constrain on mass to the SV fit computation e.
g --M=125.0

Once the job have finished the .tar files can be copied using the command:

 python scripts/copy_crab_outputs.py --folder=/path/to/target/directory/ --dcache_dir=/path/to/dcache/output/directory/

which assumes the target directroy has the corret subdirectory structure for the systematic shifted folders. This script also check if the .tar files exists before copying it over so exisiting files won't be overwritten.

The following script can be used to check that the number of .tar output fils matched the number of SV fit input files:

./scripts/check_copied.sh /path/to/input/files/ /path/to/output/tarfiles/

This script will also unntar the output files. If the numbers don't match you shoud re-run the copying script.


## latest instructions to run SV fit efficienctly (follow these ones!)

in the IC analysis code HiggsTauTau/scripts directory there are scripts named "hadd_smsummer17_svfit.py" and "hadd_smsummer16_svfit.py". These scripts combine SV-fit input files for each sample into 1 file. Copying over larger numbers of files to the dcache area is very slow so it is better to run these scripts initially to reduce the number of files. Run these scripts using:

  `./scripts/hadd_smsummer17_svfit.py --folder=/vols/cms/dw515/Offline/output/SM/Oct24_2017_SVFit/`

Next create a directory on your dcache area where you would like to copy the svfit input files to e.g:
  `mkdir SVFit_inputs`
cd into that directroy:
  `cd SVFit_inputs`
You then need to make a subdirectory for each systematic shift, use a command such as:

  `mkdir TSCALE_DOWN; mkdir TSCALE_UP; mkdir TSCALE0PI_UP; mkdir TSCALE0PI_DOWN; mkdir TSCALE1PI_UP; mkdir TSCALE1PI_DOWN; mkdir TSCALE3PRONG_UP; mkdir TSCALE3PRONG_DOWN; mkdir JES_UP; mkdir JES_DOWN; mkdir MET_SCALE_UP; mkdir MET_SCALE_DOWN; mkdir MET_RES_UP; mkdir MET_RES_DOWN; mkdir EFAKE0PI_UP; mkdir EFAKE0PI_DOWN; mkdir EFAKE1PI_UP; mkdir EFAKE1PI_DOWN; mkdir MUFAKE0PI_UP; mkdir MUFAKE0PI_DOWN; mkdir MUFAKE1PI_UP; mkdir MUFAKE1PI_DOWN; mkdir METUNCL_UP; mkdir METUNCL_DOWN; mkdir ESCALE_UP; mkdir ESCALE_DOWN; mkdir JESFULL_DOWN; mkdir JESFULL_UP; mkdir JESCENT_UP; mkdir JESCENT_DOWN; mkdir JESHF_UP; mkdir JESHF_DOWN; mkdir JESRBAL_UP; mkdir JESRBAL_DOWN; mkdir JESRSAMP_UP; mkdir JESRSAMP_DOWN; mkdir JES_CORR_UP; mkdir JES_CORR_DOWN; mkdir JES_UNCORR_UP; mkdir JES_UNCORR_DOWN; mkdir JESBBEE1_DOWN; mkdir JESBBEE1_UP; mkdir JESBBEE1_UNCORR_DOWN; mkdir JESBBEE1_UNCORR_UP; mkdir JESBBEE1_CORR_DOWN; mkdir JESBBEE1_CORR_UP; mkdir JESEE2_DOWN; mkdir JESEE2_UP; mkdir JESEE2_UNCORR_DOWN; mkdir JESEE2_UNCORR_UP; mkdir JESEE2_CORR_DOWN; mkdir JESEE2_CORR_UP;`

copy inputs and submit jobs using this script:

  `python scripts/submit_crab_jobs_new.py --folder=/vols/cms/dw515/Offline/output/SM/Oct01_SVFit/ --dcache_dir=/store/user/dwinterb/Oct01_SVFit/ --crab=Oct01_SVFit --copy`

after the jobs have finished copy the output over using:
  `nohup python -u scripts/copy_crab_outputs.py --folder=/vols/cms/dw515/Offline/output/SM/Oct01_SVFit/ --dcache_dir=/store/user/dwinterb/SVFit/ --crab=Oct01_SVFit`

untar the files using:
  `scripts/CheckTar.sh /vols/cms/dw515/Offline/output/SM/Oct01_SVFit/`
this script will also print the total number of files untarred, I suggest checking that this number matches the number of task submitted. If it does not match then some jobs may not have been copied over correctly and so you should run the copy_crab_outputs.py script again
