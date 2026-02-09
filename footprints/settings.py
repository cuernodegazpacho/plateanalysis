import os


DATAPATH = '/Users/busko/Projects/VASCO_data/footprints'


# current_dataset = '19012,19019'   # 2400  1938-02-18 20:15:32 1938-02-19 22:49:10  next night
# current_dataset = '16643,16646'   # 1200  1922-09-26 20:37:35 1922-09-26 22:09:21  same nigth
# current_dataset = '17328,17337'   # 3600  1927-04-05 01:53:31 1927-04-28 22:50:24  3 weeks later
# current_dataset = '18947,18949'   # 1200  1937-11-02 18:46:34 1937-11-02 19:56:23  same night
# current_dataset = '62330,62343'   # 1500  1944-04-14 21:34:49 1944-05-11 21:49:20  1 month later
# current_dataset = '63438,63440'   #  900  1952-09-16 23:24:11 1952-09-18 00:04:08  two nights later
# current_dataset = '9528,9553'     #  600  1957-05-20 23:47:07 1957-05-31 00:07:53  2 weeks later
current_dataset = '9319,9320'     #  900  1956-12-03 20:27:18 1956-12-03 20:55:56  same night  - CANDIDTE
# current_dataset = '9318,9319'     # same night - this and all below
# current_dataset = '9317,9318      
# current_dataset = '9316,9317'
# current_dataset = '9315,9316'
# current_dataset = '9313,9315'
# current_dataset = '9321,9322'
# current_dataset = '9322,9323'
# current_dataset = '9323,9324
# current_dataset = '9324,9325'     # same night
# current_dataset = '9325,9326'     #   -   possible candidate
# current_dataset = '9326,9327'
# current_dataset = '9327,9328'
# current_dataset = '9344,9345'
# current_dataset = '9345,9346'
# current_dataset = '9346,9347'
# current_dataset = '9347,9348'
# current_dataset = '9348,9349'
# current_dataset = '9349,9350'


def fname(name, datapath=DATAPATH):
    return os.path.join(datapath, name)


images = {
    '19012': 'S05379_y.fits',
    '19019': 'S05386_y.fits',
    '16643': 'S02865_y.fits',
    '16646': 'S02868_y.fits',
    '17328': 'S03679_y.fits',
    '17337': 'S03688_y.fits',
    '18947': 'S05313_y.fits',
    '18949': 'S05315_y.fits',
    '62330': 'DRP0174_x.fits',
    '62343': 'DRP0187_x.fits',
    '63438': 'DR01413_y.fits',
    '63440': 'DR01415_y.fits',
    '9528':  'GS00987_x.fits',
    '9553':  'GS01012_x.fits',
    '9313':  'GS00762_x.fits',
    '9315':  'GS00764_x.fits',
    '9316':  'GS00765_x.fits',
    '9317':  'GS00766_x.fits',
    '9318':  'GS00767_x.fits',
    '9319':  'GS00768_x.fits',
    '9320':  'GS00769_x.fits',
    '9321':  'GS00770_x.fits',
    '9322':  'GS00771_x.fits',
    '9323':  'GS00772_x.fits',
    '9324':  'GS00773_x.fits',
    '9325':  'GS00774_x.fits',
    '9326':  'GS00775_x.fits',
    '9327':  'GS00776_x.fits',
    '9328':  'GS00777_x.fits',
    '9344':  'GS00783_x.fits',
    '9345':  'GS00784_x.fits',
    '9346':  'GS00785_x.fits',
    '9347':  'GS00786_x.fits',
    '9348':  'GS00787_x.fits',
    '9349':  'GS00788_x.fits',
    '9350':  'GS00789_x.fits',
}


# these functions replaced a (much simpler) dict with static parameters,
# and is used for keeping backwards compatibility throughout the code.

def get_table_psf_nomatch(plate1, plate2):
        return 'table_psf_nomatch_' + str(plate1) + '_' + str(plate2) + '.fits'

def get_parameters(key):
    par = parameters['default'] | parameters[key]
    
    plate1 = key.split(',')[0]
    plate2 = key.split(',')[1]

    par['table1'] = 'sources_' + plate1 + '.csv'
    par['table2'] = 'sources_' + plate2 + '.csv'
    par['table1_calib'] = 'sources_calib_' + plate1 + '.csv'
    par['table2_calib'] = 'sources_calib_' + plate2 + '.csv'
    par['table_matched'] = 'table_match_' + plate1 + '_' + plate2 + '.fits'
    par['table_non_matched'] = 'table_nomatch_' + plate1 + '_' + plate2 + '.fits'
    par['table_psf_nonmatched'] = get_table_psf_nomatch(plate1, plate2)
    
    par['image1'] = images[plate1]
    par['image2'] = images[plate2]
                                                                                  
    return par


parameters = {
    'default': {
        'nproc': 8,                                # number of performance processors (Mac M1)
        'sextractor_flags': 4,
        'model_prediction': 0.8,
        'max_flux_threshold': 0.3,
        'elongation': 1.5,                         # less than
        'annular_bin': 5,                          # less or equals
        'flag_rim': 0,
        'nbrighter': 150000,
        'sampling_step': 10,  
        'min_acceptable_flux': 15000,
        'min_fwhm':  5.,
        'max_fwhm': 10.,
        'qfit_max': 5.,
        'cfit_max': 5.,
        'invert_east':  [False,False],
        'invert_north': [False,False],
    },
    # 1m-Spiegelteleskop
    '19012,19019': {
        'sextractor_flags': 8,
        'model_prediction': 0.5,
        'annular_bin': 1,
        'sampling_step': 1,
        'min_acceptable_flux': 12000,
        'min_fwhm': 10.,
        'max_fwhm': 17.,
    },
    '16643,16646': {
        'sextractor_flags': 8,
        'annular_bin': 8,
        'elongation': 1.5,
        'model_prediction': 0.5,
        'annular_bin': 1,
        'sampling_step': 1,  
        'min_fwhm': 6.,
    },
    '17328,17337': {
        'sextractor_flags': 8,
        'elongation': 1.5,
        'model_prediction': 0.5,
        'annular_bin': 1,
        'sampling_step': 1,
        'min_acceptable_flux': 25000,
        'min_fwhm': 7.5,
        'invert_east':  [False,True],
        'invert_north': [False,True],
    },
    '18947,18949': {
        'sextractor_flags': 8,
        'model_prediction': 0.5,
        'elongation': 1.5,
        'annular_bin': 1,
        'sampling_step': 1,
        'min_acceptable_flux': 20000,
        'min_fwhm': 9.,
    },    
    # Doppel-Reflektor
    '62330,62343': {
        'annular_bin': 8,
        'max_flux_threshold': 0.3,
        'sampling_step': 1,
        'min_acceptable_flux': 20000,
        'min_fwhm': 7.5,
        'max_fwhm': 13.,
    },
    '63438,63440': {
        'annular_bin': 8,
        'max_flux_threshold': 0.3,
        'sampling_step': 1,
        'min_acceptable_flux': 25000,
        'min_fwhm': 6.,
        'max_fwhm': 9.,
    },
    # Grosser Schmidt-Spiegel
    '9528,9553': {
        'annular_bin': 8,
        'sampling_step': 50,
        'min_acceptable_flux': 25000,
        'max_fwhm': 7.5,
    },
    # candidate
    '9319,9320': {
        'annular_bin': 4,
        'min_acceptable_flux': 25000,
        'max_fwhm': 7.5,
    },
    '9318,9319': {              
        'annular_bin': 4,
        'sampling_step': 5,
        'min_acceptable_flux': 25000,
        'max_fwhm': 15.,
    },
    '9317,9318': {              
        'annular_bin': 4,
        'sampling_step': 5,
        'min_acceptable_flux': 25000,
        'max_fwhm': 15.,
    },
    '9316,9317': {              
        'annular_bin': 4,
        'sampling_step': 5,
        'max_fwhm': 15.,
    },
    '9315,9316': {              
        'annular_bin': 4,
        'sampling_step': 5,
        'min_acceptable_flux': 23000,
    },
    '9313,9315': {              
        'sampling_step': 5,
        'min_acceptable_flux': 20000,
    },
    '9321,9322': {              
        'min_acceptable_flux': 20000,
        'max_fwhm': 15.,
    },
    '9322,9323': {              
        'sampling_step': 5,
        'min_acceptable_flux': 20000,
        'max_fwhm': 15.,
    },
    '9323,9324': {              
        'min_acceptable_flux': 25000,
    },
    '9324,9325': {              
        'sampling_step': 5,
    },
    # possible candidate
    '9325,9326': {              
        'min_acceptable_flux': 25000,
    },
    '9326,9327': {              
        'min_acceptable_flux': 30000,
        'max_fwhm': 15.,
    },
    '9327,9328': {              
        'min_acceptable_flux': 25000,
    },
    '9344,9345': {
        'sampling_step': 4,
    },
    '9345,9346': {
        'sampling_step': 2,
        'max_fwhm': 15.,
    },
    '9346,9347': {                # maybe a candidate?
        'sampling_step': 3,
        'min_fwhm': 6.5,
        'max_fwhm': 15.,
    },
    '9347,9348': {
        'sextractor_flags': 8,
        'annular_bin': 7,
        'max_flux_threshold': 0.2,
        'elongation': 1.7, 
        'sampling_step': 4,
        'max_fwhm': 15.,
    },
    '9348,9349': {
        'sextractor_flags': 8,
        'annular_bin': 7,
        'max_flux_threshold': 0.2,
        'elongation': 1.7, 
        'sampling_step': 8,
        'min_fwhm':  7.,
        'max_fwhm': 15.,
    },
    '9349,9350': {
        'sextractor_flags': 8,
        'annular_bin': 7,
        'max_flux_threshold': 0.2,
        'elongation': 1.7, 
        'sampling_step': 8,
        'min_fwhm':  7.,
        'max_fwhm': 15.,
    },
}


# Plate IDs in interesting sequences of images. This dict was built 
# by script footprint_analysis.ipynb. This dict is for telescope 
# Grosser Schmidt-Spiegel and includes only at least 3 plates taken 
# on the same night, and overlapping more than 50% in area.

sequences = {
    'seq 00': [8794, 8795, 8796],
    'seq 01': [9167, 9168, 9169],
    'seq 02': [9245, 9246, 9247],
    'seq 03': [9313, 9315, 9316, 9317, 9318, 9319, 9320],        # processed  -  candidate
    'seq 04': [9321, 9322, 9323, 9324, 9325, 9326, 9327, 9328],  # processed
    'seq 05': [9344, 9345, 9346, 9347, 9348, 9349, 9350],        # processed
    'seq 06': [9341, 9342, 9343],
    'seq 07': [9473, 9474, 9475],
    'seq 08': [9488, 9489, 9490, 9491, 9492],
    'seq 09': [9521, 9522, 9523],
    'seq 10': [9531, 9533, 9534, 9535, 9536],
    'seq 11': [9534, 9535, 9536, 9537, 9538, 9539, 9540, 9543],
    'seq 12': [9542, 9543, 9544, 9545, 9546, 9547, 9548, 9549],
    'seq 13': [9550, 9551, 9552],
    'seq 14': [9553, 9555, 9556, 9557, 9558],
}







