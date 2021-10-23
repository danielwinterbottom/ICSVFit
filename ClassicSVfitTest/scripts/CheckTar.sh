inloc=$1


dirs=("" "TSCALE0PI_UP" "TSCALE0PI_DOWN" "TSCALE1PI_UP" "TSCALE1PI_DOWN" "TSCALE3PRONG_UP" "TSCALE3PRONG_DOWN" "TSCALE3PRONG1PI0_UP" "TSCALE3PRONG1PI0_DOWN" "JER_UP" "JER_DOWN" "MET_SCALE_UP" "MET_SCALE_DOWN" "MET_RES_UP" "MET_RES_DOWN" "EFAKE0PI_DOWN" "EFAKE0PI_UP" "EFAKE1PI_DOWN" "EFAKE1PI_UP" "MUFAKE0PI_DOWN" "MUFAKE0PI_UP" "MUFAKE1PI_DOWN" "MUFAKE1PI_UP" "MUSCALE_DOWN" "MUSCALE_UP" "ESCALE_DOWN" "ESCALE_UP" "METUNCL_UP" "METUNCL_DOWN" "JESRBAL_DOWN" "JESRBAL_UP" "JESABS_DOWN" "JESABS_UP" "JESABS_YEAR_DOWN" "JESABS_YEAR_UP" "JESFLAV_DOWN" "JESFLAV_UP" "JESBBEC1_DOWN" "JESBBEC1_UP" "JESBBEC1_YEAR_DOWN" "JESBBEC1_YEAR_UP" "JESEC2_DOWN" "JESEC2_UP" "JESEC2_YEAR_DOWN" "JESEC2_YEAR_UP" "JESHF_DOWN" "JESHF_UP" "JESHF_YEAR_DOWN" "JESHF_YEAR_UP" "JESRELSAMP_YEAR_DOWN" "JESRELSAMP_YEAR_UP")


cwd=$(pwd)
for i in "${dirs[@]}"; do
  cd $inloc/$i

  #N=$(ls -1 svfit_output*_tar.root | wc -l)
  N=$(ls -1 *.tar | wc -l)
    
  for j in $(ls *.tar); do
    echo untarring $j in directory $i
    tar -xvf $j
  done

  for j in $(ls *_tar_*.root); do
    echo untarring $j in directory $i
    tar -xvf $j
  done

  echo $i: $N

  cd $cwd
done

cd $cwd
