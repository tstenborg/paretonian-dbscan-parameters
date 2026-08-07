"""Import and filter Geoscience Australia magnetic and gravity survey netCDF data."""

import logging
import os
import sys
from importlib.metadata import PackageNotFoundError, requires, version
from pathlib import PurePosixPath
from urllib.parse import urlsplit

# Third-party imports.
import requests
import xarray as xr
from packaging.requirements import Requirement


##############################################################################

# Logger configuration. Output all messages of level INFO and higher.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function definitions.


def package_available(package_name: str) -> bool:
    """Check if a package and its dependencies are available."""
    try:
        # Get the package's dependencies.
        str_dependencies = requires(package_name)
    except PackageNotFoundError:
        logger.critical("Package '%s' needs installation.", package_name)
        return False

    # If the package has no dependencies, exit check early.
    if not str_dependencies:
        return True

    dependencies_ok = True
    for str_dep_check in str_dependencies:
        req_check = Requirement(str_dep_check)

        # Don't bother checking optional dependencies.
        if req_check.marker and "extra" in str(req_check.marker):
            continue

        try:
            # Check if the dependency is installed.
            installed_version = version(req_check.name)

            # Check if the installed version is correct.
            if not installed_version in req_check.specifier:
                logger.critical(
                    "Package '%s' needs to be at version %s.",
                    req_check.name,
                    req_check.specifier,
                )
                dependencies_ok = False

        except PackageNotFoundError:
            logger.critical(
                "Package '%s', version %s, needs installation.",
                req_check.name,
                req_check.specifier,
            )
            dependencies_ok = False

    return dependencies_ok


##############################################################################

# Check that indirect dependencies and supporting packages are available.
if not package_available("dask"):
    sys.exit(1)
if not package_available("netCDF4"):
    sys.exit(1)


# Grav data:     Gravmap2019-grid-grv_cscba.nc
# Grav_1vd data: Gravmap2019-grid-grv_cscba_1vd.nc
# Mag data:      ?

# Ensure the target data file is reachable.
# Grav data.
#str_url = "https://thredds.nci.org.au/thredds/fileServer/iv65/Geoscience_Australia_Geophysics_Reference_Data_Collection/national_geophysical_compilations/Gravmap2019/Gravmap2019-grid-grv_cscba.nc"
# Grav_1vd data.
str_url = "https://thredds.nci.org.au/thredds/fileServer/iv65/Geoscience_Australia_Geophysics_Reference_Data_Collection/national_geophysical_compilations/Gravmap2019/Gravmap2019-grid-grv_cscba_1vd.nc"
try:
    response = requests.get(str_url, stream=True)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    logger.critical("HTTP error: %s", err)
    sys.exit(1)
except Exception as err:
    logger.critical("Error: %s", err)
    sys.exit(1)

# Perform cross-platform-safe file name extraction from the URL.
str_url_path = urlsplit(str_url).path
str_filename = PurePosixPath(str_url_path).name
str_filename_stem = PurePosixPath(str_url_path).stem

# Download the netCDF data in chunks to avoid loading it all into memory.
# N.B. The file will automatically close after the with block.
# N.B. "wb" is "write binary" mode.
with open(str_filename, "wb") as data_file:
    logger.info("Downloading data...")
    for chunk in response.iter_content(chunk_size=8192):
        # Write normal data chunks, not keep-alive heartbeat chunks.
        if chunk:
            data_file.write(chunk)
    logger.info("Download complete.")
data_file.close() # Explicit close, even though scoped to the 'with' block.
response.close()


# Open the netCDF file with automatically-determined optimal chunk sizes.
with xr.open_dataset(str_filename, chunks="auto") as ds:
    # Drop the "crs" (coordinate reference system) column, it's unneeded.
    ds = ds.drop_vars("crs")

    # Filter the data to a geographical region of interest.
    # Save it to a Pandas dataframe.
    # N.B. Direct Xarray dataset to CSV conversion isn't supported.
    logger.info("Filtering data...")
    filtered_df = ds.where(
        (ds.lat >= -21.32401265) & (ds.lat <= -20.88236365) & (ds.lon >= 140.5298547) & (ds.lon <= 140.8115101), drop=True
    ).to_dataframe().reset_index()
ds.close() # Explicit close, even though scoped to the 'with' block.

# Remove the full downloaded netCDF dataset.
os.remove(str_filename)

# Rename Pandas dataframe column names.
filtered_df.rename(
    columns={"lat": "Lat", "lon": "Lon", "Band1": "Grav_1vd"},
    inplace=True
)

# Save the filtered data from Pandas to CSV format.
# N.B. Suppress row numbers with "index=False".
filtered_df.to_csv(f"filtered_{str_filename_stem}.csv", index=False)
logger.info("Filtering complete.")


# Double check the grav_1vd metadata still matches what's in the data description document.

################################################################################

## Release unneeded memory.
#del filtered_df
#gc.collect()

## Import magnetic and gravity survey data.
## The data contains now duplicate rows.
## Split the data and drop unneeded columns.
#logger.info("Importing data.")
#data_file = Path(__file__).resolve().parent.parent / "data" / "mag-grav-grav1vd.csv"
#data_subset = subset_data_pandas(csv_to_pandas(data_file), bool_split=False)

## Centre and scale the data using the median and quantiles.
## N.B. RobustScaler will convert Pandas dataframes into arrays.
#logger.info("Scaling data.")
#data_scaled = RobustScaler().fit(data_subset).transform(data_subset)
#del data_subset

## Convert back to Pandas.
#data_scaled = pd.DataFrame(data_scaled, columns=["Mag", "Grav_1vd"])


## Visualise the data distributions.
##
## Plot height is specified in inches.
## Try height of 20% of A4 width = 0.2 * 210 mm = 42 mm = 42/25.4 inches.
#PLOT_HEIGHT = 42 / 25.4
#BUILD_PLOTS = False


## DBSCAN clustering.
#logger.info("Clustering data (%s data points).", str(data_scaled.shape[0]))
#min_samples = recommend_min_neighbors(data_dimensionality=data_scaled.shape[1])
#eps = recommend_eps(
#    data_input=data_scaled,
#    min_neighbors=min_samples,
#    diagnostic_plots=BUILD_PLOTS,
#    plot_height=PLOT_HEIGHT,
#)

## Release unneeded memory.
#del PLOT_HEIGHT
#gc.collect()

#data_dbs = DBSCAN(eps=eps, min_samples=min_samples)
#data_dbs.fit(data_scaled)  # Perform clustering.
#dbs_labels = data_dbs.labels_ + 1

## Prepare to save results.
#logger.info("Saving results.")
#output_file_prefix = (
#    data_file.stem + "_dbscan_rs_e" + str(eps) + "_m" + str(min_samples)
#)
## Re-retrieve.
#data_subset = subset_data_pandas(csv_to_pandas(data_file), bool_split=False)

## Save labels.
#output_file = output_file_prefix + "_labels.csv"
#np.savetxt(
#    output_file,
#    np.c_[data_subset, data_scaled, dbs_labels],
#    delimiter=",",
#    header="Mag,Grav_1vd,Mag_scaled,Grav_1vd_scaled,Cluster_label",
#    comments="",
#)

## Save clusters.
#for idx in range(1, max(dbs_labels) + 1):
#    output_data = data_subset[dbs_labels == idx]
#    output_file = output_file_prefix + "_cluster" + str(idx) + ".csv"
#    np.savetxt(
#        output_file,
#        output_data,
#        delimiter=",",
#        header="Mag,Grav_1vd",
#        comments="",
#    )
#logger.info("Clusters found: %s", str(idx))

## Save outliers.
#output_data = data_subset[dbs_labels == 0]
#output_file = output_file_prefix + "_outliers.csv"
#np.savetxt(output_file, output_data, delimiter=",", header="Mag,Grav_1vd", comments="")
#logger.info("Outliers found: %s", str(output_data.shape[0]))

#logger.info("\nProgram complete.")
