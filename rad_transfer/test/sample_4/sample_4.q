#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --job-name=mcfost-lightcurve_4
#SBATCH --output=mcfost-lightcurve_4M.qout
#SBATCH --time=0-2:00:00
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

mcfost systempara.para -df densityfile.fits -fix_star -star_bb
mcfost systempara.para -df densityfile.fits -fix_star -star_bb -img 4.4484
mcfost systempara.para -df densityfile.fits -fix_star -star_bb -img 4.6
mcfost systempara.para -df densityfile.fits -fix_star -star_bb -img 4.708
mcfost systempara.para -df densityfile.fits -fix_star -star_bb -img 4.8828
mcfost systempara.para -df densityfile.fits -fix_star -star_bb -img 5.0454
mcfost systempara.para -df densityfile.fits -fix_star -star_bb -img 5.11247
mcfost systempara.para -df densityfile.fits -fix_star -star_bb -img 5.27426
