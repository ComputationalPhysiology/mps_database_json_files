# Library for loading json files
import json

# Library for working with Path - makes it easy to work with paths on Mac and Windows
from pathlib import Path

# Library for plotting - install with 'pip install matplotlib'
import matplotlib.pyplot as plt

# Utility functions from utils.py
import utils


# Specify path to the file
folder = Path("example_data")

# ID in json filename
id = "20221021-103614"

# Path to folder
path = folder / f"mps-data-{id}.json"

# Directory where to put the figures
outdir = Path("figures") / f"{id}"
outdir.mkdir(exist_ok=True, parents=True)

if not path.is_file():
    raise FileNotFoundError(f"File {path} not found")

# Load json file into a python object (a list)
all_data = json.loads(path.read_text())

print(f"Number of entries: {len(all_data)}")

# Pick out the first element
data = all_data[0]

# Print some info
print(f"Keys: {data.keys()}")
print(f"Tags: {data['analysis_tags']}, Current tag: {data['current_tag']}")
utils.print_dict(data, "attributes", "Attributes")
utils.print_dict(data, "analysis_settings", "Fluorescence settings")
utils.print_dict(data, "features", "Features")
utils.print_dict(data, "motion_tracking_settings", "Motion tracking settings")
utils.print_dict(data, "motion_features", "Motion Features")


# Plot unchopped fluorescence data
unchopped_data = data.get("unchopped_data", {})
utils.plot_trace(
    unchopped_data, "original_times", "original_trace", outdir / "original_trace.png"
)
utils.plot_trace(unchopped_data, "times", "trace", outdir / "corrected_trace.png")

# Plot chopped fluorescence data
chopped_data = data.get("chopped_data", {})
fig, ax = plt.subplots()
for beat_nr in range(data["features"]["num_beats"]):
    ax.plot(
        chopped_data.get(f"time_{beat_nr}", []),
        chopped_data.get(f"trace_{beat_nr}", []),
    )
fig.savefig(outdir / "beats.png")

utils.plot_trace(chopped_data, "time_all", "trace_all", outdir / "average_all.png")
utils.plot_trace(chopped_data, "time_1std", "trace_1std", outdir / "average_1std.png")


# Get motion data
motion_data = data.get("motion_tracking", {})
utils.plot_motion_trace(motion_data, "displacement_norm", outdir)
# utils.plot_motion_trace(motion_data, "displacement_x", outdir)
# utils.plot_motion_trace(motion_data, "displacement_y", outdir)
utils.plot_motion_trace(motion_data, "velocity_norm", outdir)
# utils.plot_motion_trace(motion_data, "velocity_x", outdir)
# utils.plot_motion_trace(motion_data, "velocity_y", outdir)
