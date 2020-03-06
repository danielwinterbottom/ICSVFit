#!/bin/bash
# example usage:
# ./scripts/copy_from_dcache.sh path1 path2
# path1 is the path to the dcache directroy containing the outputs - this is the directroy before the 'dated' directory e.g '/store/user/dwinterb/SVFit/Nov25_SVFitMETCL_DOWN/' (which contains subdirectory(s) such as '171127_200039/')
# path2 is the path to which the files will be copied
# The script will determine the latest subdirectory of path1 by comparing the dates/times in the directory name and then search all the subdirectroies (e.g 0000/ 0001/ 0002/ ...) for outputs and copy them to path2
export path1=$1
export path2=$2
export batch=$3
export job_name=$4

times_per_job=20

date_names=($(xrdfs gfe02.grid.hep.ph.ic.ac.uk:1097 ls $path1 | cut -d"/" -f2-))
    export most_recent=0
    for k in "${date_names[@]}"; do
      date=$(echo $k | rev | cut -d"/" -f1 | rev | cut -d"_" -f1)$(echo $k | rev | cut -d"/" -f1 | rev | cut -d"_" -f2-) 
      if [[ $date > $most_recent ]]; then 
        export most_recent_string=$k
        most_recent=$date
      fi
done


directories=($(xrdfs gfe02.grid.hep.ph.ic.ac.uk:1097 ls $most_recent_string))
export count=0
n_times=0
job_num=0
echo $most_recent_string
for path1 in "${directories[@]}"; do
  filelist=($(xrdfs gfe02.grid.hep.ph.ic.ac.uk:1097 ls /$path1/ | grep tar | rev | cut -d"/" -f1 | rev))
  export dir=$(pwd)
  none_in_dir=1
  if [[ $(ls -a $path2 | grep svfit_output | grep .tar) != "" ]]; then 
    none_in_dir=0;
    list=$(ls $path2/svfit_output*.tar)
  fi
  for i in "${filelist[@]}"; do
    if [[ $list  == *"$i"* ]] && [ $none_in_dir == 0 ] ; then continue; fi #if already in directory then skip
    ((count++))
    export fullpath1=srm://gfe02.grid.hep.ph.ic.ac.uk:8443/srm/managerv2?SFN=/pnfs/hep.ph.ic.ac.uk/data/cms//$path1/$i
    export fullpath2=$path2/$i
    if [ $batch == 1 ]; then
      if [ $n_times == 0 ]; then 
        job=$(echo job_copy_from_dcache_"$job_name"_"$job_num".sh)
        echo cd $dir > $job
        echo source /vols/grid/cms/setup.sh > $job
        echo "export SCRAM_ARCH=slc6_amd64_gcc481" >> $job
        echo "eval \`scramv1 runtime -sh\`" >> $job
        echo "ulimit -c 0" >> $job
        echo lcg-cp $fullpath1 $fullpath2 >> $job
        ((n_times++))
      else 
        echo lcg-cp $fullpath1 $fullpath2 >> $job
        ((n_times++))
        if [ $n_times == $times_per_job ]; then
           chmod 755 $job
           qsub -q hep.q -l h_rt=0:180:0 -cwd $job
           ((job_num++))
           n_times=0
        fi
      fi
    else 
      lcg-cp $fullpath1 $fullpath2
    fi
  done
done
if [ $batch == 1 -a $count != 0 ]; then
  chmod 755 $job
  qsub -q hep.q -l h_rt=0:180:0 -cwd $job
fi 
  echo Total files copied: $count


