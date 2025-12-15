import argparse
import numpy as np
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="anneal schedule CSV")
    ap.add_argument("--out", default="an.png")
    ap.add_argument("--title", default="Annealing Schedule (distance vs temperature)")
    args = ap.parse_args()

    data = np.genfromtxt(args.csv, delimiter=",", names=True)
    T = data["temp"] if "temp" in data.dtype.names else data["T"]

    best = data["best_km"]
    cur = data["current_km"]

    plt.figure(figsize=(8, 5))
    plt.plot(T, best, label="best")
    plt.plot(T, cur, label="current", linewidth=0.7)
    plt.xscale("log")
    plt.gca().invert_xaxis()
    plt.xlabel("temperature")
    plt.ylabel("distance (km)")
    plt.title(args.title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.out, dpi=200)
    print("Wrote", args.out)

if __name__ == "__main__":
    main()
