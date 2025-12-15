import matplotlib.pyplot as plt
import numpy as np
import argparse

def load_xy(filename):
    """Load only first two columns, skipping lines beginning with '#'."""
    data = []
    with open(filename) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            cols = line.split()
            data.append([float(cols[0]), float(cols[1])])
    data.append(data[0])  # close the path
    return np.array(data)

def load_polygons(filename):
    """Load lon/lat polygons separated by blank lines."""
    polygons = []
    current = []

    with open(filename) as f:
        for line in f:
            line = line.strip()

            if not line:
                if current:
                    polygons.append(np.array(current))
                    current = []
                continue

            parts = line.split()
            lon = float(parts[0])
            lat = float(parts[1])
            current.append([lon, lat])

    if current:
        polygons.append(np.array(current))

    return polygons

def make_plot(infile, optfile=None, region="NA", outpdf=None, before=None, after=None):
    # Load data
    polygons = load_polygons("world_50m.dat")
    # polygons = load_polygons("world.dat")  # low res

    cities_orig = load_xy(infile)
    cities_out = load_xy(optfile) if optfile else None

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot world map
    for poly in polygons:
        ax.plot(poly[:, 0], poly[:, 1], color="black", lw=0.8)

    # Plot initial path only for small N (avoid clutter for 1k/2k)
    if len(cities_orig) < 300:
        ax.plot(cities_orig[:, 0], cities_orig[:, 1],
                lw=1, color="red", alpha=0.35, label="initial path")

    # Plot optimized path (thinner for big N)
    if cities_out is not None:
        npts = len(cities_out)
        if npts > 300:
            lw = 0.7
            ms = 1.2
        else:
            lw = 2
            ms = 3

        ax.plot(cities_out[:, 0], cities_out[:, 1],
                lw=lw, color="blue", marker='o', markersize=ms, label="optimized path")

    ax.set_title("Plot of Salesman's Cities")
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")

    # Axis ranges
    if region == "World":
        ax.set_xlim(-180, 180)
        ax.set_ylim(-90, 90)
    else:
        ax.set_xlim(-180, -60)
        ax.set_ylim(10, 75)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend
    ax.legend(loc="upper right")

    # Distance text box
    if before is not None and after is not None:
        txt = f"Initial: {before:.1f} km\nAfter SA: {after:.1f} km"
        ax.text(
            0.02, 0.02, txt,
            transform=ax.transAxes,
            fontsize=10,
            bbox=dict(boxstyle="round", alpha=0.85)
        )

    # Save plot
    if outpdf is None:
        outpdf = infile.split('.')[0] + '.pdf'

    plt.tight_layout()
    plt.savefig(outpdf, format='pdf', facecolor='white')
    print("Wrote", outpdf)

def usage():
    print('usage:')
    print('python routeplot.py cities.dat [route.dat] -w --out cities.pdf --before X --after Y')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='route plotter')
    parser.add_argument('paths', nargs='*', help='original cities file [optimized route file]')
    parser.add_argument("-w", action='store_true', help="plot the whole world (default NA)")
    parser.add_argument("--out", default=None, help="output pdf name (e.g. cities150.pdf)")
    parser.add_argument("--before", type=float, default=None, help="initial distance (km)")
    parser.add_argument("--after", type=float, default=None, help="optimized distance (km)")
    args = parser.parse_args()

    if len(args.paths) < 1:
        print("at least one input file needed")
        usage()
        raise SystemExit(1)

    cities = args.paths[0]
    cities2 = args.paths[1] if len(args.paths) > 1 else None
    region = "World" if args.w else "NA"

    make_plot(cities, cities2, region, outpdf=args.out, before=args.before, after=args.after)





