inloc=$1
outloc=$2
dirs=('' 'TSCALE_UP' 'TSCALE_DOWN' 'TSCALE0PI_UP' 'TSCALE0PI_DOWN' 'TSCALE1PI_UP' 'TSCALE1PI_DOWN' 'TSCALE3PRONG_UP' 'TSCALE3PRONG_DOWN' 'EFAKE0PI_UP' 'EFAKE0PI_DOWN' 'EFAKE1PI_UP' 'EFAKE1PI_DOWN' 'MUFAKE0PI_UP' 'MUFAKE0PI_DOWN' 'MUFAKE1PI_UP' 'MUFAKE1PI_DOWN' 'METUNCL_UP' 'METUNCL_DOWN' 'METCL_UP' 'METCL_DOWN' 'MUSCALE_UP' 'MUSCALE_DOWN' 'ESCALE_UP' 'ESCALE_DOWN')
cwd=$(pwd)
for i in "${dirs[@]}"; do
  echo "subdirectory: "$i
  cd $inloc/$i
  Ninputs=$(ls -1 *input*.root | wc -l)
  cd $cwd  
  cd $outloc/$i

  if [ $Ninputs == $(ls -1 svfit_output*.tar | wc -l) ]; then 
    echo "inputs = outputs for subdirectory: "$i
    for j in $(ls *.tar); do
      tar -xvf $j
    done

  else 
    echo "inputs != outputs for subdirectory: "$i
  fi

  cd $cwd
done

cd $cwd
