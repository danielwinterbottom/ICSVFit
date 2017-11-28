#!/bin/bash
export path1=$1
export path2=$2
filelist=($(xrd gfe02.grid.hep.ph.ic.ac.uk:1097 ls /$path1/ | grep .tar | rev | cut -d"/" -f1 | rev))
export dir=$(pwd)
export count=0
for i in "${filelist[@]}"; do
  ((count++))
  export fullpath1=srm://gfe02.grid.hep.ph.ic.ac.uk:8443/srm/managerv2?SFN=/pnfs/hep.ph.ic.ac.uk/data/cms//$path1/$i
  export fullpath2=$path2/$i/
  lcg-cp $fullpath1 $fullpath2
done
echo Total files copied: $count

