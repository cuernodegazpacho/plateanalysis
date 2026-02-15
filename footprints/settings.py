import os
import json


DATAPATH = '/Users/busko/Projects/VASCO_data/footprints'
# DATAPATH = '/Volumes/backup/plateanalysis_data/footprints'


# keep these in here just for convenience. The pipeline code
# handles this, but for running notebooks manually, set the
# desired dataset key in file dataset.json

# current_dataset = '19012,19019'   # 2400  1938-02-18 20:15:32 1938-02-19 22:49:10  next night
# current_dataset = '16643,16646'   # 1200  1922-09-26 20:37:35 1922-09-26 22:09:21  same nigth
# current_dataset = '17328,17337'   # 3600  1927-04-05 01:53:31 1927-04-28 22:50:24  3 weeks later
# current_dataset = '18947,18949'   # 1200  1937-11-02 18:46:34 1937-11-02 19:56:23  same night
# current_dataset = '62330,62343'   # 1500  1944-04-14 21:34:49 1944-05-11 21:49:20  1 month later
# current_dataset = '63438,63440'   #  900  1952-09-16 23:24:11 1952-09-18 00:04:08  two nights later
# current_dataset = '9528,9553'     #  600  1957-05-20 23:47:07 1957-05-31 00:07:53  2 weeks later
# current_dataset = '9319,9320'     #  900  1956-12-03 20:27:18 1956-12-03 20:55:56  same night  - CANDIDTE
# current_dataset = '9318,9319'     # same night - this and all below
# current_dataset = '9317,9318      
# current_dataset = '9316,9317'
# current_dataset = '9315,9316'
# current_dataset = '9313,9315'
# current_dataset = '9321,9322'
# current_dataset = '9322,9323'
# current_dataset = '9323,9324
# current_dataset = '9324,9325'
# current_dataset = '9325,9326'     #   -   possible candidate
# current_dataset = '9326,9327'
# current_dataset = '9327,9328'
# current_dataset = '9344,9345'
# current_dataset = '9345,9346'
# current_dataset = '9346,9347'
# current_dataset = '9347,9348'
# current_dataset = '9348,9349'
# current_dataset = '9349,9350'
# current_dataset = '9537,9538'


# To support pipleine mode, the current data set
# name is kept in a json file.
dataset_json = 'dataset.json'
try:
    json_file = open(dataset_json, 'r')
    dataset_dict = json.load(json_file)
    current_dataset = dataset_dict['current_dataset']
except FileNotFoundError:
    print(f"Error: File {images_json} was not found.")
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")
    

# Image names are kept in a json file so the download
# code can update it with new image names as soon as
# images are downloaded.
images_json = 'images.json'
try:
    json_file = open(images_json, 'r')
    images = json.load(json_file)

except FileNotFoundError:
    print(f"Error: File {images_json} was not found.")
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")

    
# these functions replace a (much simpler) dict with static parameters,
# and are used for keeping backwards compatibility throughout the code.

def fname(name, datapath=DATAPATH):
    return os.path.join(datapath, name)

def get_table_sources(plate1, calib=False):
    prefix = 'sources_'
    if calib:
        prefix = prefix + 'calib_'
    return prefix + str(plate1) + '.csv'

def get_table_psf_nomatch(plate1, plate2):
    return 'table_psf_nomatch_' + str(plate1) + '_' + str(plate2) + '.fits'

def get_parameters(key):
    par = parameters['default']
    if key in parameters:
        par = par | parameters[key]
    
    plate1 = key.split(',')[0]
    plate2 = key.split(',')[1]

    par['table1'] = get_table_sources(plate1)
    par['table2'] = get_table_sources(plate2)
    par['table1_calib'] = get_table_sources(plate1, calib=True)
    par['table2_calib'] = get_table_sources(plate2, calib=True)
    par['table_matched'] = 'table_match_' + plate1 + '_' + plate2 + '.fits'
    par['table_non_matched'] = 'table_nomatch_' + plate1 + '_' + plate2 + '.fits'
    par['table_psf_nonmatched'] = get_table_psf_nomatch(plate1, plate2)
    
    par['image1'] = images[plate1]
    par['image2'] = images[plate2]
                                                                                  
    return par


# Parameters that may require fine tuning, specific to each dataset.
# The defaults are, for now,  more appropriate to Grosser Schmidt-Spiegel 
# datasets, since we are focussing on that telescope in particular. 

parameters = {
    'default': {
        'nproc': 8,                                # number of performance processors (Mac M1)
        'sextractor_flags': 4,
        'model_prediction': 0.8,
        'max_flux_threshold': 0.3,
        'elongation': 1.5,                         # less than
        'annular_bin': 5,                          # less or equals
        'flag_rim': 0,
        'min_acceptable_flux': 10000,
        'min_fwhm':  5.,
        'max_fwhm': 15.,
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
        'min_fwhm': 6.,
    },
    '17328,17337': {
        'sextractor_flags': 8,
        'elongation': 1.5,
        'model_prediction': 0.5,
        'annular_bin': 1,
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
        'min_acceptable_flux': 15000,
        'min_fwhm': 8.,
    },    
    # Doppel-Reflektor
    '62330,62343': {
        'annular_bin': 8,
        'max_flux_threshold': 0.3,
        'min_acceptable_flux': 20000,
        'min_fwhm': 7.5,
        'max_fwhm': 13.,
    },
    '63438,63440': {
        'annular_bin': 8,
        'max_flux_threshold': 0.3,
        'min_acceptable_flux': 25000,
        'min_fwhm': 6.,
        'max_fwhm': 9.,
    },
    # Grosser Schmidt-Spiegel
    '9528,9553': {
        'annular_bin': 8,
        'min_acceptable_flux': 25000,
        'max_fwhm': 7.5,
    },
    '9319,9320': {                         # candidate
        'annular_bin': 6,
        'min_acceptable_flux': 20000,
        'min_fwhm': 4.0,
        'max_fwhm': 10.,
    },
    '9318,9319': {              
        'annular_bin': 4,
        'min_acceptable_flux': 25000,
        'max_fwhm': 15.,
    },
    '9317,9318': {              
        'annular_bin': 4,
        'min_acceptable_flux': 25000,
        'max_fwhm': 15.,
    },
    '9316,9317': {              
        'annular_bin': 4,
        'max_fwhm': 15.,
    },
    '9315,9316': {              
        'annular_bin': 4,
        'min_acceptable_flux': 23000,
    },
    '9313,9315': {              
        'min_acceptable_flux': 20000,
    },
    '9321,9322': {              
        'min_acceptable_flux': 20000,
        'max_fwhm': 15.,
    },
    '9322,9323': {              
        'min_acceptable_flux': 20000,
        'max_fwhm': 15.,
    },
    '9323,9324': {              
        'min_acceptable_flux': 25000,
    },
    '9324,9325': {              
    },
    '9325,9326': {                          # possible candidate
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
    },
    '9345,9346': {
        'max_fwhm': 15.,
    },
    '9346,9347': {                         # maybe a candidate?
        'min_fwhm': 6.5,
        'max_fwhm': 15.,
    },
    '9347,9348': {
        'sextractor_flags': 8,
        'annular_bin': 7,
        'max_flux_threshold': 0.2,
        'elongation': 1.7, 
        'max_fwhm': 15.,
    },
    '9348,9349': {
        'sextractor_flags': 8,
        'annular_bin': 7,
        'max_flux_threshold': 0.2,
        'elongation': 1.7, 
        'min_fwhm':  7.,
        'max_fwhm': 15.,
    },
    '9349,9350': {
        'sextractor_flags': 8,
        'annular_bin': 7,
        'max_flux_threshold': 0.2,
        'elongation': 1.7, 
        'min_fwhm':  7.,
        'max_fwhm': 15.,
    },
}


# Plate IDs in interesting sequences of images. This dict was built 
# by script footprint_analysis.ipynb. This dict is for telescope 
# Grosser Schmidt-Spiegel and includes only at least 3 plates taken 
# on the same night, and overlapping more than 50% in area.

# BEWARE that the plate ID sequence number does not necessarily 
# corresponds with the time sequence. Script footprint_analysis.ipynb 
# is not yet sorting then by time, but by plate ID number. Manual 
# editing of the lists below may still needed to place plate IDs in
# the proper temporal order.

sequences = {
    'seq 00': [8794, 8795, 8796],
    'seq 01': [9167, 9168, 9169],
    'seq 02': [9245, 9246, 9247],
    'seq 03': [9313, 9315, 9317, 9318, 9319, 9320, 9316],        # processed  -  candidate
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

