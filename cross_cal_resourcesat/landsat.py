import rasterio, os, math, glob, shutil
import numpy as np

def meta_l8(path, keyword):

    """ 
    This function reads the metadata file of the LISS III and AWiFS images and returns the value of the keyword provided.
    Parameters:
            path (str): path to folder containing the radiance image and the *_META.txt file
            keyword (str): keyword to be searched in the metadata file

    Returns:
            meta (float): value of the keyword
    """

    try:
    
        file = open(glob.glob(os.path.join(path, '*_MTL.txt'))[0]).readlines()
        meta = ""
        
        for lines in file:
            if keyword in lines:
                meta = float(lines.split("=")[-1].strip())
        return meta
    
    except:
        print('No MTL.txt file found.')
 

def landsat_ref(inpf, inp_file):

    """
    This function converts Landsat 8 radiance image into reflectance image.

    Parameters:
            inpf (str): Path to folder containing Landsat 8 radiance and MTL.txt file
            inp_file (str): Name of the file

    Returns:
            opf (str): Path of the output folder. 
    """
    
    opf = os.path.join(inpf, 'Reflectance')
    os.makedirs(opf, exist_ok = True)
    
    with (rasterio.open)(os.path.join(inpf, inp_file)) as (r):
        toa = r.read(1).astype('float32')
        param = r.profile
    toa[toa == 0] = np.nan
    param.update(dtype = 'float32')

    esun = meta_l8(inpf, 'EARTH_SUN_DISTANCE')
    reflectance_mult_band = meta_l8(inpf, 'REFLECTANCE_MULT_BAND_1')
    reflectance_add_band = meta_l8(inpf, 'REFLECTANCE_ADD_BAND_1')
    sun_elev_deg = meta_l8(inpf, 'SUN_ELEVATION')

    ''' Ref: https://www.usgs.gov/landsat-missions/using-usgs-landsat-level-1-data-product '''
    
    toa_reflectance = ((reflectance_mult_band * toa) + reflectance_add_band)/math.sin(math.radians(sun_elev_deg))

    toa_reflectance[toa_reflectance>=1] = np.nan
    toa_reflectance[toa_reflectance<0] = 0
    if (np.nanmax(toa_reflectance) <= np.nanpercentile(toa_reflectance, 99.99)):
        toa_reflectance = toa_reflectance
    else:
        toa_reflectance[toa_reflectance>=np.nanpercentile(toa_reflectance, 99.99)] = np.nanpercentile(toa_reflectance, 99.999)

    with (rasterio.open)((os.path.join(opf, inp_file)), 'w', **param) as (w):
        w.write(toa_reflectance, 1)

    return opf