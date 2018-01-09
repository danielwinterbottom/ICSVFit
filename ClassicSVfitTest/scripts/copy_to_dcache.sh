#!/bin/bash
# example usage:
# ./scripts/copy_to_dcache.sh path1 path2
# path1 is the path to the directory containing the .root files to be copied
# path2 is the path to the dcahe directory
export path1=$1
export path2=$2
export batch=$3
export job_name=$4

times_per_job=40

export count=0
n_times=0
job_num=0
  export dir=$(pwd)
  for i in $(ls $path1/ | grep input*.root); do
    ((count++))
    export fullpath2=srm://gfe02.grid.hep.ph.ic.ac.uk:8443/srm/managerv2?SFN=/pnfs/hep.ph.ic.ac.uk/data/cms/$path2/$i
    export fullpath1=$path1/$i
    if [ $batch == 1 ]; then
      if [ $n_times == 0 ]; then 
        job=$(echo job_copy_to_dcache_"$job_name"_"$job_num".sh)
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
if [ $batch == 1 ]; then
  if [ -z "$job" ]; then 
    chmod 755 $job
    qsub -q hep.q -l h_rt=0:180:0 -cwd $job
  fi
fi 
  echo Total files copied: $count

