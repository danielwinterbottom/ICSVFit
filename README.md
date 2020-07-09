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
git clone git@github.com:SVfit/ClassicSVfit TauAnalysis/ClassicSVfit
cd TauAnalysis/ClassicSVfit
git checkout release_2018Mar20
cd ../../
git clone git@github.com:SVfit/SVfitTF TauAnalysis/SVfitTF
```

clone ICSVFit package
```
git clone git@github.com:danielwinterbottom/ICSVFit.git ICSVFit/
```
cd ICSVFit/ClassicSVfitTest
git checkout fix_crab 
cd ../../

build 
```
scram b -j8
```


## latest instructions to run SV fits on the grid (follow these ones!)

In the IC analysis code HiggsTauTau/scripts directory there are scripts named "scripts/hadd_legacy16_svfit.py", "hadd_smsummer17_svfit.py", and "hadd_smsummer18_svfit.py". These scripts combine SV-fit input files for each sample into 1 file. Copying over larger numbers of files to the dcache area is very slow so it is better to run these scripts initially to reduce the number of files. Run these scripts using:

  `./scripts/hadd_smsummer17_svfit.py --folder=/vols/cms/dw515/Offline/output/SM/Oct24_2017_SVFit/`

Note if you are running SVfits for different samples not listed in these scripts, then you need to add the sample named to these scripts otherwise they will not get hadded!

Then copy the input files over to dcache area:

First create nominal output folder in dCache:

    `uberftp sedsk53.grid.hep.ph.ic.ac.uk 'mkdir store/user/<user>/<dest>'`

Then run copying script -- put -r creates the required subdirectories if needed.

    `uberftp sedsk53.grid.hep.ph.ic.ac.uk 'put -r /vols/cms/<source>/ store/user/<user>/<dest>/'`


Then submit the jobs over the grid using:

  `python scripts/submit_crab_jobs_new.py --folder=/vols/cms/dw515/Offline/output/SM/Oct01_SVFit/ --dcache_dir=/store/user/dwinterb/Oct01_SVFit/ --crab=Oct01_SVFit `

after the jobs have finished copy the output over using:
  `python -u scripts/copy_crab_outputs.py --folder=/vols/cms/dw515/Offline/output/SM/Oct01_SVFit/ --dcache_dir=/store/user/dwinterb/SVFit/ --crab=Oct01_SVFit`

untar the files using:
  `scripts/CheckTar.sh /vols/cms/dw515/Offline/output/SM/Oct01_SVFit/`
this script will also print the total number of files untarred, I suggest checking that this number matches the number of task submitted. If it does not match then some jobs may not have been copied over correctly and so you should run the copy_crab_outputs.py script again


## Alternative method of copying output files from dCache to /vols/cms/

First create /vols/cms/ destination folder if required.
    `mkdir /vols/cms/<dest>/`

Then run uberftp command to copy from dCache:
    `uberftp sedsk53.grid.hep.ph.ic.ac.uk 'get -r store/user/<user>/<source>/ /vols/cms/<dest>/'`

this will copy the directory structure that is produced by crab so you will need move the outputs over to the correct output directories (i.e for each systematics folder) 
