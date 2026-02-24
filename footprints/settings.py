import os
import json


DATAPATH = '/Users/busko/Projects/VASCO_data/footprints'
# DATAPATH = '/Volumes/backup/plateanalysis_data/footprints'


# To support pipleine mode, the current data set name is kept in a 
# json file. To run scripts manually, edit this file to point to the
# desired plate pair (careful with editing, JSON files have finicky
# syntax). The pipeline overwrites this file.

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
    par['table_candidates'] = 'table_candidates_' + plate1 + '_' + plate2 + '.fits'
    
    par['image1'] = images[plate1]
    par['image2'] = images[plate2]
    
    return par


# Parameters that may require fine tuning, specific to each dataset.
# The defaults are, for now,  more appropriate to Grosser Schmidt-Spiegel 
# datasets, since we are focussing on that telescope in particular. 

parameters = {
    'default': {
        'nproc': 8,                                # number of performance processors (Mac M1)
        # sextractor criteria
        'sextractor_flags': 8,
        'model_prediction': 0.6,
        'elongation': 1.5,                         # less than
        'annular_bin': 5,                          # less or equals
        'flag_rim': 0,
        # PSF analysis
        'max_flux_threshold': 0.1,
        'min_acceptable_flux': 500,
        'min_fwhm':  4.,
        'max_fwhm': 15.,
        'qfit_max': 4.,
        'cfit_max': 0.003,
        'neighborhood_cutout_size': 7.,           # full side of square, arcmin
        # display
        'display_cutout_size': 1.,                # full side of square, arcmin
        'profile_diff_threshold': 0.04,           # checked with false positives
        'elongation_limit': 1.2,
        'plot_limit': 100,
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
}


# Plate IDs in interesting sequences of images. This dict was built 
# by script footprint_analysis.ipynb (it has to be manually copied and
# pasted from the output of that script, in here). 
# 
# This dict is for telescope Grosser Schmidt-Spiegel and includes only 
# at least 3 plates taken on the same night, and overlapping more than 
# 50% in area.

# BEWARE that the plate ID sequence number may not necessarily 
# corresponds with the time sequence. Script footprint_analysis.ipynb 
# may not yet be correctly sorting then by time. Manual editing of the 
# lists below may still be needed in order to place plate IDs in the 
# proper temporal sequence.

sequences = {
    'seq00': [8794, 8795, 8796],
    'seq01': [9245, 9246, 9247],
    'seq03': [9313, 9315, 9317, 9318, 9319, 9320],              # processed  -  candidate
    'seq04': [9322, 9323, 9324, 9325, 9326, 9327, 9328],        # processed
    'seq05': [9344, 9345, 9346, 9347, 9348, 9349, 9350],        # processed
    'seq06': [9341, 9342, 9343],
    'seq07': [9473, 9474, 9475],
    'seq08': [9521, 9522, 9523],
    'seq09': [9533, 9534, 9535],
    'seq10': [9538, 9539, 9540],
    'seq11': [9545, 9546, 9547],
    'seq12': [9550, 9551, 9552],
}
    
    
        
    
    
