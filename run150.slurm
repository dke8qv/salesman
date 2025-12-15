#!/bin/bash
#SBATCH --time=02:00:00
#SBATCH -A phys56xx
#SBATCH --partition=standard
#SBATCH --job-name=tsp150
#SBATCH --output=tsp150_%j.log
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G


source ~/.bashrc
56xx


make

# run
./sales cities150.dat route150.dat an150.csv





echo "done"