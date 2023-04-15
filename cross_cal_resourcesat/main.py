from cross_cal_resourcesat.cross_cal_resourcesat import do_calibration

def main():

    reference_sensor = input('Enter the name of the reference sensor ["Sentinel 2", "Landsat 8", "Others"]: ')
    inpf_liss = input('Enter the path to the folder containing the radiance images of LISS III or AWiFS [inpf_liss]: ')
    if reference_sensor == 'Others':
        print('Note: If "reference_sensor" is "Others", "inpf_ref" should be the path to reflectance images.')
    inpf_ref = input('Enter the path to the folder containing the reference images [inpf_ref]:')

    do_calibration(inpf_liss = inpf_liss, inpf_ref = inpf_ref, reference_sensor = reference_sensor)

if __name__ == '__main__':
    main()
