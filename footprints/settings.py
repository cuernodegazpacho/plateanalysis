import os
import json


DATAPATH = '/Users/busko/Projects/VASCO_data/footprints'
# DATAPATH = '/Volumes/backup/plateanalysis_data/footprints'

CATALOG = 'footprints_5.csv'
RESULTS = "./results/"


# To support pipleine mode, the current data set and sequence names
# are kept in a json file. To run scripts manually, edit this file 
# to point to the desired plate pair (careful with editing, JSON 
# files have finicky syntax). The pipeline overwrites this file.

dataset_json = 'dataset.json'    
try:
    with open(dataset_json, 'r', encoding='utf-8-sig') as json_file:
        dataset_dict = json.load(json_file)
        current_dataset  = dataset_dict['current_dataset']
        current_sequence = dataset_dict['current_sequence']
except FileNotFoundError:
    print(f"Error: File {dataset_json} was not found.")
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
# The defaults are, for now,  more appropriate to the longer sequences
# of the Grosser Schmidt-Spiegel datasets, since we are focussing on 
# that telescope in particular. 

parameters = {
    'default': {
        'nproc': 8,                                # number of performance processors (Mac M1 16Gb) - average tasks
        'nproc_analysis': 3,                       # number of performance processors (Mac M1 16Gb) - heavy tasks
        # sextractor criteria
        'sextractor_flags': 8,
        'model_prediction': 0.6,
        'elongation': 1.5,                         # less than
        'annular_bin': 9,                          # less or equals
        'flag_rim': 0,
        # analysis
        'fwhm_init': 8.,
        'fit_shape': 31,
        'max_flux_threshold': 0.1,
        'min_acceptable_flux': 500,
        'min_fwhm':  3.,
        'max_fwhm': 15.,
        'qfit_max': 2.5,
        'cfit_max': 0.003,
        'neighborhood_cutout_size': 8.0,          # full side of square, arcmin
        'elongation_limit': 1.2,
        'profile_diff_threshold': 0.05,           # 0.04 good, checked with false positives
        'circularity_threshold': [70],            # about 28% on a 0-255 scale
        'circularity_low_limit': 0.80, 
        'tiny_cutout_size': 21,                   # for cicularity computation (px)
        'false_positive_threshold': 10.,          # checked with false positives
        # display
        'display_cutout_size': 1.5,               # full side of square, arcmin
        'plot_limit': 100,
        'rotate': [False,False],                  # rotate *before* flipping - NOT IMPLEMENTED YET
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
    '9341,9342': {
        'nproc_analysis': 6,
        'max_flux_threshold': 0.03,
        'annular_bin': 5,
    },
    '9342,9343': {
        'nproc_analysis': 6,
        'max_flux_threshold': 0.03,
        'annular_bin': 5,
    },
    '9474,9475': {
        'nproc_analysis': 4,
        'min_fwhm':  5.,
        'max_fwhm': 10.,
        'annular_bin': 5,
    },
    '9039,9040': {
        'rotate': [False,True],      # 2nd plate has to be reprojected for display
    },
    '9012,9013': {
        'display_cutout_size': 7.0,        # full side of square, arcmin
        'neighborhood_cutout_size': 15.0,  # full side of square, arcmin
    },
    '9095,9096': {
        'annular_bin': 7,                  # 9096 looks dirty and underexposed
        'display_cutout_size': 4.0,       
        'neighborhood_cutout_size': 15.0, 
    },
    '9099,9100': {
        'annular_bin': 7,                 
        'display_cutout_size': 4.0,       
        'neighborhood_cutout_size': 15.0, 
    },
    '9337,9338': {
        'annular_bin': 6,                  # focus
        'display_cutout_size': 4.0,       
        'neighborhood_cutout_size': 15.0, 
    },
    '9352,9353': {
        'annular_bin': 6,                  # focus
        'display_cutout_size': 4.0,       
        'neighborhood_cutout_size': 15.0, 
    },
    '9355,9356': {                         # 9356 partially blocked by shutter
        'annular_bin': 6,                  # focus
        'display_cutout_size': 4.0,       
        'neighborhood_cutout_size': 15.0, 
    },
    '9528,9529': {
        'annular_bin': 8,
    },
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
#     'seq00': [8794, 8795, 8796],                                # out-of-focus (but good for testing)
    'seq01': [9245, 9246, 9247],
    'seq03': [9313, 9315, 9317, 9318, 9319, 9320],      
    'seq04': [9322, 9323, 9324, 9325, 9326, 9327, 9328],
    'seq05': [9344, 9345, 9346, 9347, 9348, 9349, 9350],
    'seq06': [9341, 9342, 9343],
    'seq07': [9473, 9474, 9475],
#     'seq08': [9521, 9522, 9523],                                # comet - trailed
    'seq09': [9533, 9534, 9535],
    'seq10': [9538, 9539, 9540],
    'seq11': [9545, 9546, 9547],
    'seq12': [9550, 9551, 9552],
# two-plate sequences that overlap by more than 50% in area.
    'seq13': [8874, 8875],
#     'seq14': [9039, 9040],    # 9040 is Y only, rotated AND flipped
    'seq15': [9012, 9013],
    'seq16': [9016, 9017],
    'seq17': [9095, 9096],
    'seq18': [9099, 9100],
#     'seq19': [9167, 9168, 9169],   # out-of-order
    'seq20': [9168, 9169],
    'seq21': [9174, 9175],
    'seq22': [9176, 9177],
    'seq23': [9228, 9229],
    'seq24': [9233, 9234],
    'seq25': [9305, 9306],
    'seq26': [9285, 9286],
    'seq27': [9337, 9338],
    'seq28': [9352, 9353],
    'seq29': [9355, 9356],
#     'seq30': [9469, 9472],    # comet Arend-Roland   Ha + GG5
#     'seq31': [9482, 9484],    # comet Arend-Roland   Kodak OaO
#     'seq32': [9488, 9489, 9490, 9491],     # comet Arend-Roland   Kodak OaO
#     'seq33': [9525, 9526],     # comet Arend-Roland partial tail
    'seq34': [9528, 9529],
#     'seq35': [9536, 9537],   # comet Arend-Roland   Kodak OaO
#     'seq36': [9543, 9544],   # comet Arend-Roland   Kodak OaO
    'seq37': [9548, 9549],
    'seq38': [9555, 9556],
    'seq39': [9557, 9558],     # coordinates a bit off?
#     'seq40': [9596, 9597],     # comet Mrkos Ha+GG5, OaO (?)
}

    
        
    
    
