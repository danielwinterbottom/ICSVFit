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

