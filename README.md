# cross_cal_resourcesat


[![image](https://img.shields.io/pypi/v/cross_cal_resourcesat.svg)](https://pypi.python.org/pypi/cross_cal_resourcesat)
[![image](https://img.shields.io/conda/vn/conda-forge/cross_cal_resourcesat.svg)](https://anaconda.org/conda-forge/cross_cal_resourcesat)
[![Python Versions](https://img.shields.io/pypi/pyversions/ocm2.svg)](https://pypi.org/project/cross_cal_resourcesat/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![image](https://github.com/opengeos/leafmap/workflows/docs/badge.svg)](https://github.com/akhi9661/cross_cal_resourcesat)

---

## Introduction

This code module applies a simple cross calibration on LISS III and AWiFS to calibrate them with the help
of a reference image like Landsat 8 and Sentinel 2.

Takes two inputs:
- `inpf_liss` = path to folder LISS III or AWiFS bands
- `inpf_ref` = path to folder containing reference image bands

Final output folder: 
- `inpf_liss\Reflectance\Calibration`

Four temporary images are also generated which are automatically deleted after the execution. These are two composite images,
one resampled image, and one clipped image
Note: Please make sure that both input and reference image have the same projection system. If not, please reproject the input.

---


## Package information
A python package to cross calibrate ResourceSat 2 sensors like LISS III, AWiFS or LISS IV.


-   Github repo: https://github.com/akhi9661/cross_cal_resourcesat
-   PypI: https://pypi.org/project/cross-cal-resourcesat/
-   Free software: MIT license
-   Documentation: https://akhi9661.github.io/cross_cal_resourcesat


Note: At the moment, if `reference_sensor  = 'Landsat 8'`, path to reflectance images will have to provided in `inpf_ref`. 
      The reprojection too is bit sketchy at the moment (defaults to `EPSG: 32643`). Will be fixed shortly.

---
## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
