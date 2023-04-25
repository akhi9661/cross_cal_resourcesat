# Usage

To use cross_cal_resourcesat in a project:

# cross_cal_resourcesat

## Introduction

This package applies a cross calibrates LISS III and AWiFS with the help of a reference image like Landsat 8 and Sentinel 2.

Takes two inputs:
- `inpf_liss` = path to folder LISS III or AWiFS bands
- `inpf_ref` = path to folder containing reference image bands. Could be Landsat 8 or Sentinel 2.

Final output folder: 
- `inpf_liss\Reflectance\Calibration`

Three temporary images are also generated which are automatically deleted after the execution. These are two composite images, and one resampled image.


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

### 1. To run the library from the command line, use:

```
python main.py
```
Enter the input as prompted.

### 2. To use the library in the program:

- First install the library.

```
pip install cross_cal_resourcesat
```
- Import the dependencies in the environment

```
import rasterio, os, re, math, glob, shutil
from osgeo import gdal, osr, gdalconst
import numpy as np
```
- Import the library
```
import cross_cal_resourcesat
```
- Set the path to uncalibrated and reference image. The path provided should be absolute path and not relative.

```
inpf_liss = r'\docs\Examples\liss'
inpf_l8 = r'\docs\Examples\ref_l8'
```
- Call the `do_calibration` function.

```
cross_cal_resourcesat.do_calibration(inpf_liss = inpf_liss, inpf_ref = inpf_l8, reference_sensor = 'Landsat 8')
```
To use other reference sensors, select `reference_sensor = 'Sentinel 2'` or `reference_sensor = 'Others'`

Note: If reference sensor, other than Landsat 8 or Sentinel 2 is used, the path `inpf_ref` should be the path to folder containing reflectance images of reference sensor and not radiance images.

---
