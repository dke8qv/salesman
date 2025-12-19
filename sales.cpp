#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <cmath>
#include <ctime>
#include <iomanip>
#include <chrono>
#include <algorithm>
#include <vector>




using namespace std;

typedef struct {
  double lon, lat;
} COORD;

static inline double urand() {
  return (rand() + 0.5) / (RAND_MAX + 1.0);
}

int GetData(const char* fname, COORD* cities, int NMAX) {
  FILE* fp = fopen(fname, "r");
  if (!fp) {
    cerr << "Error: cannot open " << fname << "\n";
    exit(1);
  }
  const int bufsiz = 1000;
  char line[bufsiz + 1];
  int ncity = 0;
  while (fgets(line, bufsiz, fp)) {
    if (line[0] == '#') continue;
    if (ncity >= NMAX) break;
    if (sscanf(line, "%lf %lf", &cities[ncity].lon, &cities[ncity].lat) == 2) {
      ncity++;
    }
  }
  fclose(fp);
  return ncity;
}

double Dist(double lat1, double lat2, double lon1, double lon2) {
  const double R = 6371.0;
  const double rad = M_PI / 180.0;
  const double dlat = (lat2 - lat1) * rad;
  const double dlon = (lon2 - lon1) * rad;
  const double la1 = lat1 * rad;
  const double la2 = lat2 * rad;

  const double s1 = sin(dlat * 0.5);
  const double s2 = sin(dlon * 0.5);
  const double a = s1 * s1 + cos(la1) * cos(la2) * (s2 * s2);
  const double c = 2.0 * atan2(sqrt(a), sqrt(1.0 - a));
  return R * c;
}

double TotalDistance(const COORD* cities, int ncity) {
  double sum = 0.0;
  for (int i = 0; i < ncity - 1; i++) {
    sum += Dist(cities[i].lat, cities[i + 1].lat, cities[i].lon, cities[i + 1].lon);
  }
  sum += Dist(cities[ncity - 1].lat, cities[0].lat, cities[ncity - 1].lon, cities[0].lon);
  return sum;
}

void CopyRoute(const COORD* src, COORD* dst, int ncity) {
  for (int i = 0; i < ncity; i++) dst[i] = src[i];
}

// Method1: swap two cities
void Method1(COORD* cities, int ncity) {
  int i = rand() % ncity;
  int j = rand() % ncity;
  while (j == i) j = rand() % ncity;
  COORD tmp = cities[i];
  cities[i] = cities[j];
  cities[j] = tmp;
}

// Method2: reverse a random segment (2-opt style)
void Method2(COORD* cities, int ncity) {
  int len = 2 + rand() % (ncity - 1);
  int start = rand() % (ncity - len + 1);

  int a = start;
  int b = start + len - 1;
  while (a < b) {
    COORD tmp = cities[a];
    cities[a] = cities[b];
    cities[b] = tmp;
    a++;
    b--;
  }
}



double EstimateT0(const COORD* cur, int ncity, double Ecur,
                  int nProbe, double factor) {
  static COORD trial[3000]; // avoid big stack allocations

  std::vector<double> dEs;
  dEs.reserve(nProbe);

  for (int k = 0; k < nProbe; k++) {
    CopyRoute(cur, trial, ncity);

    if (urand() < 0.05) Method1(trial, ncity);
    else Method2(trial, ncity);

    double Etrial = TotalDistance(trial, ncity);
    double dE = Etrial - Ecur;
    if (dE > 0.0) dEs.push_back(dE);
  }

  if (dEs.empty()) return 1.0;

  std::sort(dEs.begin(), dEs.end());
  int idx = (int)(0.90 * (dEs.size() - 1));  // 90th percentile
  double dE90 = dEs[idx];
  return factor * dE90;

}

int main(int argc, char* argv[]) {
  if (argc < 2) {
    cerr << "Usage: " << argv[0] << " cities.dat [routeout.dat] [schedule.csv]\n";
    return 1;
  }

  const char* infile = argv[1];
  const char* outRoute = (argc > 2 ? argv[2] : "route.dat");
  const char* outSched = (argc > 3 ? argv[3] : "anneal.csv");

  const int NMAX = 3000;
  COORD cur[NMAX];
  COORD trial[NMAX];
  COORD best[NMAX];

  srand((unsigned)time(nullptr));

  int ncity = GetData(infile, cur, NMAX);
  cout << "Read " << ncity << " cities from data file\n";

  auto t0 = std::chrono::steady_clock::now();

  double Ecur = TotalDistance(cur, ncity);
  int nProbe = std::min(20000, 20 * ncity); 
  double T0 = EstimateT0(cur, ncity, Ecur, nProbe, 1.2);
  cout << "Auto T0 (km): " << T0 << "  (probe moves=" << nProbe << ")\n";

  double Ebest = Ecur;
  CopyRoute(cur, best, ncity);

  cout << fixed;
  cout << "Initial distance (km): " << Ecur << "\n";

  // ---- SA parameters (tune these)
  const int steps = 12000000;        // total Metropolis trials
  //double T0 = 5000.0;            // start temperature
  //double alpha = 0.9999995;        // cooling per step 
    double Tf = 1.0; // target final temperature (km)
    double alpha = exp(log(Tf / T0) / steps);

  int printEvery = 200000;
  int schedEvery = 2000;

  ofstream sched(outSched);
  sched << "T,current_km,best_km\n";

  double T = T0;



  for (int s = 0; s < steps; s++) {
    // Make a trial configuration from current
    CopyRoute(cur, trial, ncity);

    // pick a move
    if (urand() < 0.05) Method1(trial, ncity); // occasional random swap
    else Method2(trial, ncity);                // mostly segment reverse

    double Etrial = TotalDistance(trial, ncity);
    double dE = Etrial - Ecur;

    // Metropolis acceptance vs CURRENT
    bool accept = false;
    if (dE <= 0.0) accept = true;
    else {
      double p = exp(-dE / T);
      if (urand() < p) accept = true;
    }

    if (accept) {
      CopyRoute(trial, cur, ncity);
      Ecur = Etrial;
      if (Ecur < Ebest) {
        Ebest = Ecur;
        CopyRoute(cur, best, ncity);
      }
    }

    // cool
    T *= alpha;

    if (s % schedEvery == 0) {
      sched << setprecision(12) << T << ","
            << setprecision(12) << Ecur << ","
            << setprecision(12) << Ebest << "\n";
    }

    if (s % printEvery == 0) {
      cout << "step " << s << "  T=" << setprecision(3) << T
           << "  best=" << setprecision(3) << Ebest << "\n";
    }
  }
  
  auto t1 = std::chrono::steady_clock::now();
  double sec = std::chrono::duration<double>(t1 - t0).count();


  // write best route
  ofstream out(outRoute);
  out << fixed << setprecision(6);
  for (int i = 0; i < ncity; i++) {
    out << best[i].lon << " " << best[i].lat << "\n";
  }
  out.close();
  sched.close();

  cout << fixed;
  cout << "Best distance (km):    " << setprecision(3) << Ebest << "\n";
  cout << "Runtime (s):           " << setprecision(3) << sec << "\n";
  cout << "Wrote route:           " << outRoute << "\n";
  cout << "Wrote schedule:        " << outSched << "\n";

  return 0;
}


