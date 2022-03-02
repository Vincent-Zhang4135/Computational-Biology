#!/bin/bash
#SBATCH --job-name=test
#SBATCH --time=00:00:01
#SBATCH --nodes=1
#SBATCH --account=
#SBATCH --mem-per-cpu=8192
 
# Load R
module load R

Rinfile="./CompAsn7source.R"

# Run R
Rscript $Rinfile

