Starter code and data for traveling salesman problem


Files in this directory:

* datareader.cpp : example code to read in the data files (use Makefile)
* datareader.py  : example code to read in the data files
* cities23.dat : list of coordinates for 23 cities in North America
* cities150.dat : 150 cities in North America
* cities1k.dat : 1207 cities in North America
* cities2k.dat : 2063 cities around the world
* routeplot.py : code to plot the globe and salesman's path<br>
usage:<br>
python routeplot.py cities.dat [cities2.dat] -r [="NA"],"World"'<br>
NA = North America, World = Mercator projection of the whole earth
* earth.C : (just for fun) plotting the globe in ROOT




###############Results (round-trip distance in km)###################
cities150 317298.645 48027.565 131.128
cities1k 732177.737 111461.552 1100.932
cities2k 10187617.637342 372564.206 1785.119



##########How to run########################

1] cities150: ./sales cities150.dat route150.dat an150.csv OR sbatch run150.slurm

2] cities1k: ./sales cities1k.dat route1k.dat an1k.csv OR sbatch run1k.slurm

3] cities2k: ./sales cities2k.dat route2k.dat an2k.csv OR sbatch run2k.slurm



#######################Plotting (general)###############

####Route plot (map + initial and optimized path):
    python routeplot.py <input.dat> <route_out.dat> --out <plot.pdf> \
     --before <INITIAL_KM> --after <BEST_KM>

For the world view (2k),:
    python routeplot.py cities2k.dat route2k.dat -w --out cities2k.pdf \
      --before <INITIAL_KM> --after <BEST_KM>



###Annealing schedule plots
python plot_schedule.py an150.csv --out an150.png --title an150
python plot_schedule.py an1k.csv  --out an1k.png  --title an1k
python plot_schedule.py an2k.csv  --out an2k.png  --title an2k



##########Methods###########
I use Simulated Annealing with Metropolis acceptance.
State: an ordered list of cities representing a closed tour (round trip).
Trial move types (proposal distribution):
Random swap of two cities (used occasionally, e.g. ~5%) to help escape local structure.
Random segment reversal (2-opt style) (used most of the time, e.g. ~95%) to remove crossings efficiently.
Acceptance rule (Metropolis):
Always accept if the trial tour is shorter: ΔE ≤ 0
Otherwise accept with probability exp(−ΔE / T)
Cooling schedule: exponential cooling T ← αT starting from T0, with a gentle α ≈ 1.
During the run I record T,current_km,best_km to a CSV file for plotting the annealing schedule.

