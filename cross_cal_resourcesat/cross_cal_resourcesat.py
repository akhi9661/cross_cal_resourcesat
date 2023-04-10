""" The following package contains the functions to perform cross calibration between LISS III and AWiFS and the reference image. 
"""

import rasterio, os, re, math, glob, shutil
from osgeo import gdal, osr, gdalconst
import numpy as np

def meta(inpf, keyword):

    """
    This function reads the metadata file of LISS III or AWiFS and returns the value of the keyword.
    Inputs:
        inpf = path to folder containing the metadata file
        keyword = keyword to be searched in the metadata file

    Output:
        meta = value of the keyword
    """
    
    file = open(glob.glob(os.path.join(inpf, '*_META.txt'))[0]).readlines()
    meta = ""
    
    for lines in file:
        if keyword in lines:
            meta = float(lines.split("=")[-1].strip())
    return meta

def toa_reflect(inpf, inp_name, opf, band_no):

    """
    This function converts the radiance values to reflectance values for LISS III and AWiFS. 
    Inputs:
        inpf = path to folder containing the radiance image
        inp_name = name of the radiance image
        opf = path to folder where the reflectance image will be saved
        band_no = band number of the image

    Output:
        None
    """
    
    esol = {'B2': 1849.5, 'B3': 1553.0, 'B4': 1092.0, 'B5': 239.52}
    esol_band = list(esol.values())[band_no-2]
    
    lmax, lmin, sun_elev = meta(inpf, f'B{band_no}_Lmax'), meta(inpf, f'B{band_no}_Lmin'), meta(inpf, 'SunElevationAtCenter')
    
    with rasterio.open(os.path.join(inpf, inp_name)) as r:
        param = r.profile
        toa_raw = r.read(1).astype('float32')
    
    param.update(dtype = 'float32')
    toa_raw[toa_raw == 0] = np.nan
    toa_rad = lmin + ((lmax - lmin)/1024)*toa_raw
    reflectance = (np.pi * 1 * toa_rad) / (esol_band * math.sin(math.radians(sun_elev)))
    
    reflectance[reflectance>1] = np.nan
    reflectance[reflectance<0] = np.nan
    if (np.nanmax(reflectance) <= np.nanpercentile(reflectance, 99.99)):
        reflectance = reflectance
    else:
        reflectance[reflectance>=np.nanpercentile(reflectance, 99.99)] = np.nanpercentile(reflectance, 99.999)
    
    op_name = os.path.basename(inp_name).split('.')[0] + '_ref.TIF'
    with rasterio.open(os.path.join(opf, op_name), 'w', **param) as r:
        r.write(reflectance, 1)
    
    return None

def do_ref(inpf, opf):

    """
    This function calls the `toa_reflect` function to convert the radiance values to reflectance values.
    Inputs:
        inpf = path to folder containing the radiance images
        opf = path to folder where the reflectance images will be saved

    Output:
        None
    """
    
    print('Radiance to reflectance conversion: LISS III/AWiFS.')
    
    original = os.listdir(inpf)
    gtif = list(filter(lambda x: x.endswith(("tif", "TIF", "img")), original))
    for gi in gtif:
        band_no = int(''.join(list(filter(str.isdigit, gi))))
        toa_reflect(inpf, gi, opf, band_no)
    
    return None
    
def create_multiband_image(inpf_liss, inpf_ref, files_liss, files_ref, reference_sensor = 'Sentinel 2'):

    """
    This function creates a composite image from the reflectance images of LISS III and AWiFS and the reference image.
    
    Inputs:
        inpf_liss = path to folder containing the reflectance images of LISS III or AWiFS
        inpf_ref = path to folder containing the the reference images
        files_liss = list of reflectance images of LISS III or AWiFS
        files_ref = list of reflectance images of the reference image
        reference_sensor = name of the reference sensor. Default is 'Sentinel 2'. If reference_sensor = 'Landsat 8'

    Output:
        None
    """
    
    print('Stacking: LISS III/AWiFS.')
    with rasterio.open(os.path.join(inpf_liss, files_liss[0])) as src:
        profile = src.profile
        multi_band_liss = np.zeros((profile['height'], profile['width'], len(files_liss)))

    for i, filename in enumerate(files_liss):
        with rasterio.open(os.path.join(inpf_liss, filename)) as src:
            multi_band_liss[:,:,i] = src.read(1)
            
    profile.update(count = multi_band_liss.shape[2])
    profile.update(dtype = 'float32')
    op_liss = os.path.join(inpf_liss, 'composite.TIF')
    with rasterio.open(op_liss, 'w', **profile) as dst:
        dst.write(np.rollaxis(multi_band_liss.astype(profile['dtype']), axis=2))
    dst.close()
        
    ''' Reference Image Composite '''
    
    print(f'Stacking: {reference_sensor} image.')
    with rasterio.open(os.path.join(inpf_ref, files_ref[0])) as src:
        profile = src.profile
        multi_band_ref = np.zeros((profile['height'], profile['width'], len(files_ref)))

    if reference_sensor == 'Sentinel 2':
        for i, filename in enumerate(files_ref):
            with rasterio.open(os.path.join(inpf_ref, filename)) as src:
                multi_band_ref[:,:,i] = src.read(1).astype('float32')*0.0001

    elif reference_sensor == 'Landsat 8':
        for i, filename in enumerate(files_ref):
            with rasterio.open(os.path.join(inpf_ref, filename)) as src:
                multi_band_ref[:,:,i] = src.read(1).astype('float32')
            
    profile.update(count = multi_band_ref.shape[2])
    profile.update(dtype = 'float32')
    op_ref = os.path.join(inpf_ref, 'composite_ref.TIF')
    with rasterio.open(op_ref, 'w', **profile) as dst:
        dst.write(np.rollaxis(multi_band_ref, axis=2))
    dst.close()
    
    return (op_liss, op_ref)

def do_multiband(inpf_liss, inpf_ref):

    """
    This function calls the `create_multiband_image` function to create a composite image from the reflectance images of LISS III and AWiFS and the reference image.
    
    Inputs:
        inpf_liss = path to folder containing the reflectance images of LISS III or AWiFS
        inpf_ref = path to folder containing the reflectance images of the reference image

    Output:
        None
    """
    
    original = os.listdir(inpf_liss)
    gtif_liss = list(filter(lambda x: x.endswith(("tif", "TIF", "img")), original))
    
    original = os.listdir(inpf_ref)
    gtif_ref = list(filter(lambda x: x.endswith(("tif", "TIF", "img")), original))
    
    op_liss, op_ref = create_multiband_image(inpf_liss, inpf_ref, gtif_liss, gtif_ref)
    return (op_liss, op_ref)
    
def resample_image(file_liss, file_ref):
    
    print('Resampling: LISS III to reference image')
    
    reference = gdal.Open(file_ref, 0)
    referenceTrans = reference.GetGeoTransform()
    x_res = referenceTrans[1]
    y_res = -referenceTrans[5]

    opf_resample = os.path.join(os.path.dirname(file_liss), os.path.basename(file_liss).split('.')[0] + '_resample.TIF')

    kwargs = {"format": "GTiff", "xRes": x_res, "yRes": y_res}
    ds = gdal.Warp(opf_resample, file_liss, dstSRS = 'EPSG:32643', **kwargs)
    ds = None
    
    return opf_resample
    

def calc_calibration(file_liss, file_ref):

    """
    This function calculates the calibration factors for the LISS III/AWiFS bands.
    
    Inputs:
        file_liss = path to the composite image of LISS III or AWiFS
        file_ref = path to the composite image of the reference image

    Output:
        None
    """
    
    opf_resample = resample_image(file_liss, file_ref)
    
    print('Calculating calibration factors.')

    with rasterio.open(opf_resample) as r:
        liss = r.read().astype('float32')
        param = r.profile
        print('LISS III shape:', liss.shape)
    
    param.update(count = 1)
    with rasterio.open(file_ref) as r:
        ref = r.read().astype('float32')
        print('Reference shape:', ref.shape)
        
    cal_path = os.path.join(os.path.dirname(file_liss), 'Calibrated')
    if os.path.exists(cal_path):
        shutil.rmtree(cal_path)
    os.makedirs(cal_path)
        
    num_bands = liss.shape[0]
    cal_liss = np.zeros((liss.shape[1], liss.shape[2]), dtype = 'float32')
    sbaf = []
    for i in range(num_bands):
        band_liss = liss[i,:,:]
        band_reference = ref[i,:,:]
        sbaf.append(np.nanmean(band_reference)/np.nanmean(band_liss))
        sbaf_temp = sbaf[i]
        
        print(f'Calibrating band {i+2}...')
        print('Factor:', sbaf_temp)
        cal_liss = band_liss * sbaf_temp
        opf_cal = os.path.join(cal_path, f'Band_{i+2}_cal.TIF')
        with rasterio.open(opf_cal, 'w', **param) as r:
            r.write(cal_liss, 1)

    
    os.remove(opf_resample)
    os.remove(file_liss)
    os.remove(file_ref)
    
    print("'Done'")
    return (sbaf, cal_liss, band_liss, band_reference)

def do_calibration(inpf_liss, inpf_ref):

    """
    This is the main function. 
    It calls the `do_ref` function to create the reflectance images of LISS III or AWiFS and the reference image.
    Then calls `do_mulitband` function to create layer stacks. Finally calls `calc_calibration` for calibration factors.
    
    Inputs:
        inpf_liss = path to folder containing the reflectance images of LISS III or AWiFS
        inpf_ref = path to folder containing the reflectance images of the reference image

    Output:
        None
    """

    opf = os.path.join(inpf_liss, 'Reflectance')
    if os.path.exists(opf):
        shutil.rmtree(opf)
    os.makedirs(opf)

    do_ref(inpf_liss, opf)
    
    op_liss, op_ref = do_multiband(opf, inpf_ref)
    sbaf, cal_liss, ref_liss, ref_band = calc_calibration(op_liss, op_ref)
    
    return None
