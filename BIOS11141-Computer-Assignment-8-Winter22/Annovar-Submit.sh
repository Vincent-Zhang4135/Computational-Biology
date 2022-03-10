#!/bin/sh
#SBATCH --job-name=
#SBATCH --time=05:15:00
#SBATCH --partition=broadwl
#SBATCH --ntasks-per-node=28
#SBATCH --account=bios10602

../scripts/annovar.sh ../genotyping/SRR710119.flt.vcf SRR710119