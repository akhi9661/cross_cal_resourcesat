# cross_cal_resourcesat


[![image](https://img.shields.io/pypi/v/cross_cal_resourcesat.svg)](https://pypi.python.org/pypi/cross_cal_resourcesat)
[![image](https://img.shields.io/conda/vn/conda-forge/cross_cal_resourcesat.svg)](https://anaconda.org/conda-forge/cross_cal_resourcesat)
[![Python Versions](https://img.shields.io/pypi/pyversions/ocm2.svg)](https://pypi.org/project/cross_cal_resourcesat/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![image](https://github.com/opengeos/leafmap/workflows/docs/badge.svg)](https://github.com/akhi9661/cross_cal_resourcesat)

---

## Introduction

This package applies a cross calibrates LISS III and AWiFS with the help of a reference image like Landsat 8 and Sentinel 2.

Takes two inputs:
- `inpf_liss` = path to folder LISS III or AWiFS bands
- `inpf_ref` = path to folder containing reference image bands. Could be Landsat 8 or Sentinel 2.

Final output folder: 
- `inpf_liss\Reflectance\Calibration`

Four temporary images are also generated which are automatically deleted after the execution. These are two composite images,
one resampled image, and one clipped image

---


## Package information
A python package to cross calibrate ResourceSat 2 sensors like LISS III, AWiFS or LISS IV.


-   Github repo: https://github.com/akhi9661/cross_cal_resourcesat
-   PypI: https://pypi.org/project/cross-cal-resourcesat/
-   Free software: MIT license
-   Documentation: https://akhi9661.github.io/cross_cal_resourcesat


Note: At the moment, if `reference_sensor  = 'Landsat 8'`, path to reflectance images will have to provided in `inpf_ref`. 

---
## How to use

- Clone the repository in the desired folder.

```
git clone https://github.com/akhi9661/cross_cal_resourcesat.git
```

In case this fails, download the zip file and extract it in a folder. 

- Install the required dependencies.

```
pip install -r requirements.txt
```
If it throws up an error, create a new virtual environment and install the dependencies. Installation of `GDAL` and `rasterio` is complex and generally fails in the base environment or an already existing environment. Creating a new virtual environment generally resolves this.



---
## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
