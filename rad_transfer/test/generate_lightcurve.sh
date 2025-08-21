for (( num=0; num<20; num++))
do
 cd sample_$num
 sbatch sample_$num.q
 cd ..
done
