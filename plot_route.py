import argparse
import numpy as np
import matplotlib.pyplot as plt

def read_xy(path):
    xs, ys = [], []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            xs.append(float(parts[0]))
            ys.append(float(parts[1]))
    return np.array(xs), np.array(ys)

def plot_map(mapfile):
    # map file: lon lat pairs with blank lines separating segments
    segx, segy = [], []
    with open(mapfile, "r") as f:
        for line in f:
            s = line.strip()
            if not s:
                if segx:
                    plt.plot(segx, segy, linewidth=0.6)
                    segx, segy = [], []
                continue
            if s.startswith("#"):
                continue
            lon, lat = map(float, s.split()[:2])
            segx.append(lon)
            segy.append(lat)
    if segx:
        plt.plot(segx, segy, linewidth=0.6)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("route", help="route file (lon lat per line)")
    ap.add_argument("--out", default="cities.pdf")
    ap.add_argument("--title", default="Optimized TSP Path")
    ap.add_argument("--before", type=float, required=True)
    ap.add_argument("--after", type=float, required=True)
    ap.add_argument("--map", default=None, help="map file (e.g. world.dat)")
    ap.add_argument("--xlim", nargs=2, type=float, default=None, help="xmin xmax")
    ap.add_argument("--ylim", nargs=2, type=float, default=None, help="ymin ymax")
    args = ap.parse_args()

    x, y = read_xy(args.route)

    # close the loop
    xc = np.r_[x, x[0]]
    yc = np.r_[y, y[0]]

    plt.figure(figsize=(9, 6))

    if args.map:
        plot_map(args.map)

    plt.plot(xc, yc, linewidth=0.7)
    plt.scatter(x, y, s=8)

    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.title(args.title)

    txt = f"Initial: {args.before:.1f} km\nAfter SA: {args.after:.1f} km"
    plt.gca().text(
        0.02, 0.02, txt,
        transform=plt.gca().transAxes,
        fontsize=10,
        bbox=dict(boxstyle="round", alpha=0.85)
    )

    if args.xlim:
        plt.xlim(args.xlim[0], args.xlim[1])
    if args.ylim:
        plt.ylim(args.ylim[0], args.ylim[1])

    plt.tight_layout()
    plt.savefig(args.out)
    print("Wrote", args.out)

if __name__ == "__main__":
    main()


