"""Make low-cost Pareto-like parameter estimation for sklearn's DBSCAN."""

import gc
import logging
import math
import sys
from pathlib import Path

# Third-party imports.
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import RobustScaler

##############################################################################

# Logger configuration. Output all messages of level INFO and higher.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function definitions.


def csv_to_pandas(target_file: Path) -> pd.DataFrame:
    """Import CSV data into a Pandas dataframe."""
    # Expected CSV format:
    #    col0: Lon, col1: Lat, col2: Mag, col3: Grav_1vd.
    # N.B. If the target file does not exist, exit the program.

    if not Path(target_file).is_file():
        logger.critical("File not found: %s", target_file.name)
        sys.exit(1)

    return pd.read_csv(target_file)


def recommend_eps(
    data_input: npt.NDArray[np.float64],
    min_neighbors: int,
    *,
    diagnostic_plots: bool = False,
    plot_height: float = 1.0,
) -> np.float64:
    """Get a recommended epsilon to use with DBSCAN."""
    # Low values require higher density to form a cluster.
    #     N.B. Too low yields no clusters; all points labelled as -1 for
    #          "noise".
    # Values too high clump all points into one cluster.
    #
    # Here a Pareto split (80%/20%) of the distances of a k-nearest neighbours
    # fit of all points is used.
    #
    # Input parameters:
    #     data_input         numpy array; the data set being clustered.
    #     min_neighbors      integer; number of minimum neighbors being used
    #                            with DBSCAN.
    #     diagnostic_plots   boolean; a flag triggering generation of
    #                            diagnostic plots.
    #     plot_height        float; height in inches to use for plots.

    fit_neighbors = NearestNeighbors(n_neighbors=min_neighbors).fit(data_input)

    # Find the K-neighbors of each point.
    distances, indices = fit_neighbors.kneighbors(data_input)
    del fit_neighbors
    del indices

    # Here column index 0 stores the distance between the point and itself; 0.
    # Only the distance to the nearest neighbour is needed,
    # i.e. use col index 1 (the 2nd column).
    distances = distances[:, 1]

    # Sort distances from smallest to largest.
    distances = np.sort(distances, axis=0)

    # Get the distance at the Pareto boundary.
    # Split after the first 20% smallest.
    # Splitting after the first 80% produces excessive clusters.
    num_points = data_input.shape[0]
    epsilon_estimate = distances[math.floor(num_points * 0.2)]

    if diagnostic_plots:
        # Create a distance histogram.
        logger.info(
            "Creating a distance histogram for %s data points.",
            str(num_points),
        )
        plt.axvline(epsilon_estimate)  # Overlay a vertical line for epsilon.
        sns.displot(distances, height=plot_height, aspect=1)
        plt.savefig("distances_histogram.pdf", dpi=300, pad_inches=0)

        # Create corresponding density estimates.
        sns.displot(
            distances,
            height=plot_height,
            aspect=1,
            kind="ecdf",
            linewidth=1,
        )
        plt.savefig("distances_ecdf.pdf", dpi=300, pad_inches=0)
        sns.displot(
            distances,
            height=plot_height,
            aspect=1,
            kind="kde",
            linewidth=1,
        )
        plt.savefig("distances_kde.pdf", dpi=300, pad_inches=0)
    return epsilon_estimate


def recommend_min_neighbors(data_dimensionality: int = 1) -> int:
    """Get a recommended number of minimum neighbors to use with DBSCAN."""
    # Higher values increase the density needed to form a cluster.
    # Here, the maximum is taken of:
    #    a) sklearn's default value; 5,
    #    b) twice the data dimensionality.
    #
    # Input parameters:
    #     data_dimensionality   integer; dimensionality of the data being
    #                               clustered.

    return max(5, 2 * data_dimensionality)


def subset_data_pandas(
    data_input: pd.DataFrame,
    *,
    bool_split: bool = False,
) -> pd.DataFrame:
    """Subset input Pandas data."""
    # a) Drop all columns except for Mag and Grav_1vd.
    # b) Optionally, subset the data using a coorodinate-based scheme.

    if bool_split:
        # Split the data along its coordinate mid-points.

        mid_e = (data_input[["Lon"]].max() + data_input[["Lon"]].min()) / 2
        mid_n = (data_input[["Lat"]].max() + data_input[["Lat"]].min()) / 2

        # Split by longitude.

        data_input = data_input[data_input["Lon"] <= mid_e]

        # Split by latitude.

        data_input = data_input[data_input["Lat"] <= mid_n]
    # Return data with Mag and Grav_1vd, but other columns dropped.

    return data_input.loc[:, ["Mag", "Grav_1vd"]]


##############################################################################


# Import magnetic and gravity survey data.
# The data contains now duplicate rows.
# Split the data and drop unneeded columns.
logger.info("Importing data.")
data_file = Path(__file__).resolve().parent.parent / "data" / "mag-grav1vd.csv"
data_subset = subset_data_pandas(csv_to_pandas(data_file), bool_split=False)

# Centre and scale the data using the median and quantiles.
# N.B. RobustScaler will convert Pandas dataframes into arrays.
logger.info("Scaling data.")
data_scaled = RobustScaler().fit(data_subset).transform(data_subset)
del data_subset

# Convert back to Pandas.
data_scaled = pd.DataFrame(data_scaled, columns=["Mag", "Grav_1vd"])


# Visualise the data distributions.
#
# Plot height is specified in inches.
# Try height of 20% of A4 width = 0.2 * 210 mm = 42 mm = 42/25.4 inches.
PLOT_HEIGHT = 42 / 25.4
BUILD_PLOTS = False

if BUILD_PLOTS:
    # Mag.
    sns.displot(data_scaled, x="Mag", height=PLOT_HEIGHT, aspect=1)
    plt.savefig("mag_scaled.pdf", dpi=300, pad_inches=0)

    # Grav_1vd.
    sns.displot(data_scaled, x="Grav_1vd", height=PLOT_HEIGHT, aspect=1)
    plt.savefig("grav_1vd_scaled.pdf", dpi=300, pad_inches=0)

    # 2D: Mag vs Grav_1vd.
    sns.displot(data_scaled, x="Mag", y="Grav_1vd", height=PLOT_HEIGHT, aspect=1)
    plt.savefig("2D_mag_Grav_1vd.pdf", dpi=300, pad_inches=0)

# Convert from Pandas dataframe to numpy array for processing.
data_scaled = data_scaled.to_numpy()


# DBSCAN clustering.
logger.info("Clustering data (%s data points).", str(data_scaled.shape[0]))
min_samples = recommend_min_neighbors(data_dimensionality=data_scaled.shape[1])
eps = recommend_eps(
    data_input=data_scaled,
    min_neighbors=min_samples,
    diagnostic_plots=BUILD_PLOTS,
    plot_height=PLOT_HEIGHT,
)

# Release unneeded memory.
del PLOT_HEIGHT
gc.collect()

data_dbs = DBSCAN(eps=eps, min_samples=min_samples)
data_dbs.fit(data_scaled)  # Perform clustering.
dbs_labels = data_dbs.labels_ + 1

# Prepare to save results.
logger.info("Saving results.")
output_file_prefix = (
    data_file.stem + "_dbscan_rs_e" + str(eps) + "_m" + str(min_samples)
)
# Re-retrieve.
data_subset = subset_data_pandas(csv_to_pandas(data_file), bool_split=False)

# Save labels.
output_file = output_file_prefix + "_labels.csv"
np.savetxt(
    output_file,
    np.c_[data_subset, data_scaled, dbs_labels],
    delimiter=",",
    header="Mag,Grav_1vd,Mag_scaled,Grav_1vd_scaled,Cluster_label",
    comments="",
)

# Save clusters.
for idx in range(1, max(dbs_labels) + 1):
    output_data = data_subset[dbs_labels == idx]
    output_file = output_file_prefix + "_cluster" + str(idx) + ".csv"
    np.savetxt(
        output_file,
        output_data,
        delimiter=",",
        header="Mag,Grav_1vd",
        comments="",
    )
logger.info("Clusters found: %s", str(idx))

# Save outliers.
output_data = data_subset[dbs_labels == 0]
output_file = output_file_prefix + "_outliers.csv"
np.savetxt(output_file, output_data, delimiter=",", header="Mag,Grav_1vd", comments="")
logger.info("Outliers found: %s", str(output_data.shape[0]))

logger.info("\nProgram complete.")
