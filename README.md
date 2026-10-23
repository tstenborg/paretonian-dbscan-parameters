# Low-cost Paretonian DBSCAN Parameter Estimation for Sklearn

[![super-linter](../../actions/workflows/super-linter.yml/badge.svg)](../../actions/workflows/super-linter.yml) ![human-only code](https://img.shields.io/badge/human--only-code-white)

This repository holds digital resources associated with the article "Low-cost
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

---

## Table of Contents

- [Key Files](#key-files)
- [Software Requirements](#software-requirements)
- [Getting Started](#getting-started)
- [Quality Assurance](#quality-assurance)
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

| Software                                                       | Notes                                                                                                                                                                                                                                                                                                                                    |
| :------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python                                                         | [Available here](https://www.python.org/). Free.                                                                                                                                                                                                                                                                                         |
| pip<br>&nbsp;                                                  | [Available here](https://pip.pypa.io/en/stable/). Free.<br>&nbsp;&nbsp;&nbsp;Optional but recommended.                                                                                                                                                                                                                                   |
| Python Launcher (`py`)<br>&nbsp;<br>&nbsp;<br>&nbsp;<br>&nbsp; | Optional. Free.<br>&nbsp;&nbsp;&nbsp;Arch Linux: Get with `yay -S python-launcher`<br>&nbsp;&nbsp;&nbsp;Fedora: Get with `sudo dnf install python-launcher`<br>&nbsp;&nbsp;&nbsp;Linux/Unix (general): Use [crates.io](https://crates.io/crates/python-launcher/) or Homebrew.<br>&nbsp;&nbsp;&nbsp;macOS, Windows: Bundled with Python. |

### Python Configuration

A known compatible operating environment comprises Python at the version
specified in `.python-version`, and the packages at the versions specified in
`requirements.txt`. It's recommended a Python virtual environment be created,
then the dependencies installed. Steps vary by Python development environment
and operating system, but some common options are given below.

<details>
<summary>Option 1: Python Launcher, Python and Visual Studio Code (Windows)</summary>

<!-- jscpd:ignore-start -->

<br>

From the Visual Studio Code terminal, at the repository root, create a virtual
environment:

    py -m venv .venv

(Optional) Alternatively, if you have more than one Python installation, you
can create a version-specific virtual environment. E.g., for Python 3.14.x:

    py -3.14 -m venv .venv

Once a Python virtual environment has been created, it should be linked to
Visual Studio Code.

1. Press `Ctrl + Shift + P` to open the Visual Studio Code Command Palette.

2. Type or select **Python: Select Interpreter**.

3. Select the newly created virtual environment from the drop-down list.

Lastly, from the Visual Studio Code terminal, install the dependencies:

    python -m pip install -r requirements.txt

<!-- jscpd:ignore-end -->

</details>

<details>
<summary>Option 2: Python Launcher and Python (Linux)</summary>

<!-- jscpd:ignore-start -->

<br>

From a command line, at the repository root, create a virtual environment:

    py -m venv .venv

(Optional) Alternatively, if you have more than one Python installation, you
can create a version-specific virtual environment. E.g., for Python 3.14.x:

    py -3.14 -m venv .venv

Next, activate the virtual environment:

    source .venv/bin/activate

Lastly, install the dependencies:

    python -m pip install -r requirements.txt

<!-- jscpd:ignore-end -->

</details>

<details>
<summary>Option 3: Python Launcher and Python (Windows)</summary>

<!-- jscpd:ignore-start -->

<br>

From a command line, at the repository root, create a virtual environment:

    py -m venv .venv

(Optional) Alternatively, if you have more than one Python installation, you
can create a version-specific virtual environment. E.g., for Python 3.14.x:

    py -3.14 -m venv .venv

Next, activate the virtual environment.

Windows (Command Prompt):

    .venv\Scripts\activate.bat

Windows (PowerShell):

    .venv\Scripts\Activate.ps1

Lastly, install the dependencies:

    python -m pip install -r requirements.txt

<!-- jscpd:ignore-end -->

</details>

<details>
<summary>Option 4: Python (Linux, macOS)</summary>

<br>

From a command line, at the repository root, create a virtual environment:

    python3 -m venv .venv

(Optional) Alternatively, if you have more than one Python installation, you
can create a version-specific virtual environment. E.g., for Python 3.14.x:

    python3.14 -m venv .venv

Next, activate the virtual environment:

    source .venv/bin/activate

Lastly, install the dependencies:

    python -m pip install -r requirements.txt

</details>

<details>
<summary>Option 5: Python (Windows)</summary>

<br>

From a command line, at the repository root, create a virtual environment:

    python -m venv .venv

(Optional) Alternatively, if you have more than one Python installation, you
can create a version-specific virtual environment. E.g., for Python 3.14.x
installed in `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python314\python.exe`:

    "C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python314\python.exe" -m venv .venv

Next, activate the virtual environment.

Windows (Command Prompt):

    .venv\Scripts\activate.bat

Windows (PowerShell):

    .venv\Scripts\Activate.ps1

Lastly, install the dependencies:

    python -m pip install -r requirements.txt

</details>

#### Python Package Management

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

Installing dependencies listed in `requirements.txt`:

    pip install -r requirements.txt

</details>

## Getting Started

The program `pareto_dbscan.py` should be run from Python.

    python src/pareto_dbscan.py

## Quality Assurance

The repository code has been tested in the following environment.

<details>
<summary>Windows Test Environment</summary>

<br>

| Type     | Component              | Version                                   |
| :------- | :--------------------- | :---------------------------------------- |
| Platform | Operating system       | Windows 11, 26H2 (OS Build 26300.9711)    |
| Software | Python                 | See [.python-version](.python-version).   |
| &quot;   | Visual Studio Code     | 1.143.1                                   |
| &quot;   | pip                    | 26.2.2                                    |
| Packages | Python packages        | See [requirements.txt](requirements.txt). |
| Data     | `mag-grav-grav1vd.csv` | Repository dataset.                       |

</details>

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
