import matplotlib.pyplot as plt


def print_dict(d, key, label=None):
    label = label or key
    print(f"\n{label}:")
    for name, value in d[key].items():
        print(f"{name}: {value}")


def plot(x, y, fname):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig.savefig(fname)
    plt.close("all")


def plot_trace(d, key_x, key_y, fname):
    x = d.get(key_x)
    if x is None:
        print(f"Could not find {key_x}")
        return
    y = d.get(key_y)
    if y is None:
        print(f"Could not find {key_y}")
        return
    plot(x, y, fname)


def plot_motion_trace(motion_data, key, outdir):
    time = motion_data.get("time")
    if time is None:
        print("No motion data found")
        return

    # Get data
    data = motion_data.get(key)

    # Full trace
    original = data.get("original")
    if original:
        plot(
            time[: len(original)],
            original,
            outdir / f"{key}_original.png",
        )
    # With potential background correction
    corrected = data.get("corrected")
    if corrected:
        plot(
            time[: len(corrected)],
            corrected,
            outdir / f"{key}_corrected.png",
        )

    # Beats
    chopped = data.get("chopped", {})
    fig, ax = plt.subplots()
    for t, y in zip(chopped.get("t", []), chopped.get("y", [])):
        ax.plot(t, y)
    fig.savefig(outdir / f"{key}_chopped.png")

    # Average
    plot_trace(data, "average_time", "average_trace", outdir / f"{key}_average.png")
