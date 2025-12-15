#!/bin/bash
#SBATCH --time=08:00:00
#SBATCH -A phys56xx
#SBATCH -p standard
#SBATCH --job-name=tsp2k
#SBATCH --output=tsp2k_%j.log
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G

source ~/.bashrc
56xx


make

./sales cities2k.dat route2k.dat an2k.csv




echo "done"
