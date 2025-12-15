#!/bin/bash
#SBATCH --time=02:00:00
#SBATCH -A phys56xx
#SBATCH --partition=standard
#SBATCH --job-name=tsp1k
#SBATCH --output=tsp1k_%j.log
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G


source ~/.bashrc
56xx


make

# run
./sales cities1k.dat route1k.dat an1k.csv




echo "done"

