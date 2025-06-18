#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --job-name=mcfost-transfer
#SBATCH --output=rad_transfer/apep/5shell/mcfost-transfer8.8.qout
#SBATCH --time=0-10:00:00
#SBATCH --mem=4G
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-user=ryan.white1@hdr.mq.edu.au

echo "HOSTNAME = $HOSTNAME"
echo "HOSTTYPE = $HOSTTYPE"
echo Time is `date`
echo Directory is `pwd`

ulimit -s unlimited
source ~/setup_mcfost
export OMP_NUM_THREADS=16

echo "Starting mcfost..."

mcfost wr.para -df apep_5shell_light.fits -fix_star -star_bb -root_dir rad_transfer/apep/5shell
mcfost wr.para -df apep_5shell_light.fits -fix_star -star_bb -img 8.8 -root_dir rad_transfer/apep/5shell
