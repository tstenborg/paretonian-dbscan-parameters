# Low-cost Paretonian DBSCAN Parameter Estimation for Sklearn

[![super-linter](../../actions/workflows/super-linter.yml/badge.svg)](../../actions/workflows/super-linter.yml) ![human-only code](https://img.shields.io/badge/human--only-code-white)

This repository holds digital assets associated with the article "Low-cost
Paretonian DBSCAN Parameter Estimation for Sklearn". [[1](#references)].

---

| Parameters                                        | Clusters | Outliers | Notes                                          |
| ------------------------------------------------- | -------- | -------- | ---------------------------------------------- |
| &epsilon; = 1, minPts = 20                        | &#45;    | &#45;    | Crash, exhausts memory.                        |
| &epsilon; = 0.5, minPts = 5                       | 2        | 0        | Runtime ∼ minutes. Highly asymmetric clusters. |
| &epsilon; = 9 &times; 10<sup>−4</sup>, minPts = 5 | 232      | 176,195  | Runtime ∼ seconds.                             |

Table 1. DBSCAN clustering parameter selection scheme testing. Schemes: naive
(top), sklearn default (mid), Paretonian (bottom). Test data were from magnetic
and gravity surveys at a site near Cloncurry (east of Mount Isa, Queensland).
Adapted from [[1](#references)].

---

## Table of Contents

- [Key Files](#key-files)
- [Software Requirements](#software-requirements)
- [Quality Assurance](#quality-assurance)
- [Getting Started](#getting-started)
- [Acknowledgements](#acknowledgements)
- [References](#references)

## Key Files

| File                             | Notes                                                                                     |
| :------------------------------- | :---------------------------------------------------------------------------------------- |
| `src/pareto_dbscan.py`<br>&nbsp; | Python program.<br>&nbsp;&nbsp;&nbsp;Performs parameter estimation with sklearn's DBSCAN. |
| `data/mag-grav1vd.csv`<br>&nbsp; | Test data (177,720 records, 9 KB).<br>&nbsp;&nbsp;&nbsp;Magnetic and gravity survey data. |
| `data/data-description.txt`      | Description of the test data.                                                             |
| `requirements.txt`               | Python dependencies.                                                                      |

## Software Requirements

| Software      | Notes                                                                                                  |
| :------------ | :----------------------------------------------------------------------------------------------------- |
| Python        | [Available here](https://www.python.org/). Free.                                                       |
| pip<br>&nbsp; | [Available here](https://pip.pypa.io/en/stable/). Free.<br>&nbsp;&nbsp;&nbsp;Optional but recommended. |

### Python Configuration

Please ensure the Python environment has the packages specified in
`requirements.txt` installed. A known set of compatible versions are pinned in
that file.

<details>
<summary>Windows Command Line Python Package Management</summary>

<br>

Useful Windows 11 command line syntax to use pip for Python package management
is given below. These commands assume Python is on the Windows PATH.

Checking if Python is installed:

    python --version

Checking if pip is installed:

    pip --version

Updating pip:

    python -m pip install --upgrade pip

Checking if a Python package is installed, e.g., numpy:

    pip show numpy

Showing all Python packages pip has installed:

    pip list

Installing a Python package, e.g., numpy:

    pip install numpy

Installing a Python package at a specific version, e.g., numpy 2.5.1:

    pip install numpy==2.5.1

Updating an installed Python package to a specific version, e.g., numpy 2.5.1:

    pip install --force-reinstall numpy==2.5.1

Uninstalling a Python package, e.g., numpy:

    pip uninstall numpy

</details>

## Quality Assurance

The repository code has been tested in the following environment.

<details>
<summary>Windows Test Environment</summary>

<br>

| Type     | Component              | Version                                |
| :------- | :--------------------- | :------------------------------------- |
| Platform | Operating system       | Windows 11, 25H2 (OS Build 26200.8973) |
| Software | Python                 | 3.14.16                                |
| Packages | Python packages        | See `requirements.txt`.                |
| Data     | `mag-grav-grav1vd.csv` | Repository dataset.                    |

</details>

## Getting Started

The program `pareto_dbscan.py` should be run from Python.

## Acknowledgements

This work was supported by the Australian Research Council Training Centre in
Data Analytics for Resources and Environments (project ICI9010031).

Test data source:
[Geoscience Australia Portal](https://portal.ga.gov.au/persona), by Geoscience
Australia which is &copy; Commonwealth of Australia and is provided under a
[Creative Commons Attribution 4.0 International Licence](https://creativecommons.org/licenses/by/4.0/legalcode)
and is subject to the disclaimer of warranties in section 5 of that licence.

## References

1. T. N. Stenborg and K. Silversides, "Low-cost Paretonian DBSCAN Parameter
   Estimation for Sklearn", in _Proc. Australian Data Science Network Conf.
   2022_, in Australian Data Science Network Conference Series, vol. 1,
   B. Cook, Ed., 2022, pp. 8&ndash;9.\
   [View PDF](https://www.australiandatascience.net/wp-content/uploads/2022/11/ADSN22_Proceedings.pdf)
   &nbsp; [SciX](https://scixplorer.org/abs/2022adsn.conf....8S/abstract)
