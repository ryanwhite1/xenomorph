#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --job-name=mcfost-transfer
#SBATCH --output=mcfost-transfer3.4.qout
#SBATCH --time=0-20:00:00
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
export OMP_NUM_THREADS=8

echo "Starting mcfost..."

mcfost apep.para -df apep1shell.fits -fix_star -star_bb
mcfost apep.para -df apep1shell.fits -fix_star -star_bb -img 3.4
