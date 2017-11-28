#!/bin/bash
# example usage:
# ./scripts/copy_from_dcache.sh path1 path2
# path1 is the path to the dcache directroy containing the outputs - this is the directroy before the 'dated' directory e.g '/store/user/dwinterb/SVFit/Nov25_SVFitMETCL_DOWN/' (which contains subdirectory(s) such as '171127_200039/')
# path2 is the path to which the files will be copied
# The script will determine the latest subdirectory of path1 by comparing the dates/times in the directory name and then search all the subdirectroies (e.g 0000/ 0001/ 0002/ ...) for outputs and copy them to path2
export path1=$1
export path2=$2

date_names=($(xrd gfe02.grid.hep.ph.ic.ac.uk:1097 ls $path1 | cut -d"/" -f2-))
    export most_recent=0
    for k in "${date_names[@]}"; do
      date=$(echo $k | rev | cut -d"/" -f1 | rev | cut -d"_" -f1)$(echo $k | rev | cut -d"/" -f1 | rev | cut -d"_" -f2-) 
      if [[ $date > $most_recent ]]; then
        export most_recent_string=$k
        most_recent=$date
      fi
done

directories=($(xrd gfe02.grid.hep.ph.ic.ac.uk:1097 ls $most_recent_string))
export count=0
for path1 in "${directories[@]}"; do
  filelist=($(xrd gfe02.grid.hep.ph.ic.ac.uk:1097 ls /$path1/ | grep .tar | rev | cut -d"/" -f1 | rev))
  export dir=$(pwd)
  for i in "${filelist[@]}"; do
    ((count++))
    export fullpath1=srm://gfe02.grid.hep.ph.ic.ac.uk:8443/srm/managerv2?SFN=/pnfs/hep.ph.ic.ac.uk/data/cms//$path1/$i
    export fullpath2=$path2/$i
    lcg-cp $fullpath1 $fullpath2
  done
done
echo Total files copied: $count

