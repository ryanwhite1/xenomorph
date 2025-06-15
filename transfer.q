#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=mcfost-transfer
#SBATCH --output=mcfost8.8.qout
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-user=ryan.white1@hdr.mq.edu.au
#SBATCH --time=0-8:00:00
#SBATCH --mem=4G
echo "HOSTNAME = $HOSTNAME"
echo "HOSTTYPE = $HOSTTYPE"
echo Time is `date`
echo Directory is `pwd`

ulimit -s unlimited
source ~/setup_mcfost


echo "Starting mcfost..."
mcfost wr.para -df apep_1shell.fits -fix_star -star_bb
mcfost wr.para -df apep_1shell.fits -fix_star -star_bb -img 8.8
